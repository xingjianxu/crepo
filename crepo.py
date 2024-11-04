#! /usr/bin/python
import os
import sys
import argparse
import platform
import shutil
import json
import pwd
import subprocess
from pathlib import Path
from runner import Runner


class CRepo:
    def __init__(self, args):
        self.args = args
        if not args.owner:
            args.owner = pwd.getpwuid(os.stat(self.args.repo_dir).st_uid).pw_name
        self.runner = Runner(args.dry_run, args.silent)
        self.run = self.runner.run
        self.etc_dir = os.path.join(self.args.root_dir, "etc")
        self.home_dir = os.path.join(self.args.root_dir, "home")
        self.env = {"ETC": self.etc_dir, "USER_HOME": self.args.user_home}

    def info(self, msg):
        if not self.args.silent:
            print(msg)

    def error(self, msg):
        if not self.args.silent:
            print(msg)

    def update_env(self, env):
        return self.env.update(filter(lambda x: x[1] is not None, env.items()))

    def get_default_variant():
        return platform.node().split(".")[0]

    def get_target_name_from_path(self, conf_path):
        target_name = None
        if conf_path.startswith(self.etc_dir):
            pathnames = conf_path[len(self.etc_dir) :].split(os.path.sep)
            if len(pathnames) > 1:
                target_name = pathnames[1]
        elif conf_path.startswith(self.home_dir):
            pathnames = conf_path[len(self.home_dir) :].split(os.path.sep)
            if len(pathnames) > 2:
                target_name = pathnames[2]
                if target_name == ".config":
                    target_name = pathnames[3]
                if target_name.startswith("."):
                    target_name = target_name[1:]
        if not target_name:
            return None
        target_name = Path(target_name).stem
        if target_name.endswith("rc"):
            target_name = target_name[:-2]
        return target_name

    def chown(self, file, owner):
        if sys.platform != "win32":
            shutil.chown(file, owner, -1)

    def get_target_dir(self, target_name):
        return os.path.join(self.args.repo_dir, target_name)

    def get_target_config_path(self, target_name):
        return os.path.join(self.get_target_dir(target_name), ".target.json")

    def get_target_config(self, target_name):
        target_config_path = self.get_target_config_path(target_name)
        target_config = {}
        if os.path.exists(target_config_path):
            with open(target_config_path, "r") as tcf:
                target_config = json.load(tcf)
        return target_config

    def save_target_config(self, target_name, target_config):
        with open(self.get_target_config_path(target_name), "w") as tcf:
            json.dump(target_config, tcf, sort_keys=True, indent=2)

    def get_conf_path(self, target_name, conf_name, variant):
        return os.path.join(
            self.args.repo_dir,
            target_name,
            CRepo.get_conf_name_with_variant(conf_name, variant),
        )

    def get_conf_name_with_variant(conf_name, variant):
        return (conf_name + "." + variant) if variant else conf_name

    def error_exit(self, msg, exit_code=1):
        self.error(msg)
        sys.exit(exit_code)

    def get_target_and_conf_name(self, path):
        target_name, target_name_in_path, conf_name = None, None, None
        if path.startswith("@"):
            parts = path.split("/")
            target_name_in_path = parts[0][1:]
            conf_name = "/".join(parts[1:])
        else:
            conf_name = path
        # check conflication with target name and target_name_in_path
        if (
            target_name_in_path
            and self.args.target
            and target_name_in_path != self.args.target
        ):
            self.error_exit(
                f"Target name conflict: {target_name_in_path} and {self.args.target}", 7
            )
        target_name = (
            self.args.target
            or target_name_in_path
            or ".".join(conf_name.split(".")[0:-1])
        )
        return target_name, conf_name

    def render_with_env(self, str, tmp_env={}):
        return str.format(**{**self.env, **tmp_env})

    def replace_with_env(self, str):
        if str.startswith(self.etc_dir):
            str = str.replace(self.etc_dir, "{ETC}")
        elif str.startswith(self.home_dir):
            str = os.path.join(
                "{USER_HOME}", *str[len(self.home_dir) :].split(os.path.sep)[2:]
            )
        return str

    def link_conf(
        self, target_name, conf_name, variant, permit_exec=False, required=True
    ):
        target_config = self.get_target_config(target_name)
        if not conf_name:
            target_config_keys = list(target_config.keys())
            if len(target_config_keys) == 1:
                # 如果只有一个conf，则直接使用该conf
                conf_name = target_config_keys[0]
            else:
                pairs = [(k, v) for k, v in target_config.items() if v.get("default")]
                if len(pairs) == 1:
                    conf_name = pairs[0][0]
                else:
                    self.error_exit(
                        f"Default conf definition not found: Target {target_name}, Conf {conf_name}",
                        8,
                    )

        conf_path = self.get_conf_path(target_name, conf_name, variant)
        if not os.path.exists(conf_path):
            if variant and not required:
                # 在install模式下，如果未查找到对应variant，则使用默认conf
                self.link_conf(target_name, conf_name, None, permit_exec, required)
            elif required:
                self.error_exit(
                    f"Conf file not exists: {conf_path}",
                    2,
                )
            return
        if conf_name not in target_config:
            self.error_exit(
                f"Conf definition not found: Target {target_name}, Conf {conf_name}", 3
            )
        conf_config = target_config[conf_name]

        self.update_env(
            {
                "TARGET": target_name,
                "CONF_NAME": conf_name,
                "CONF_PATH": conf_path,
                "VARIANT": variant,
            }
        )

        if permit_exec and conf_config.get("type") == "exec":
            self.info(f"Exec: Target {target_name}, Conf {conf_path}, Var {variant}")
            self.run(
                f"exec {conf_path}",
                lambda: self.exec_conf(conf_path),
            )
        else:
            origin_path = self.render_with_env(conf_config["origin"])
            self.update_env({"ORIGIN": origin_path})

            if not os.path.isdir(os.path.dirname(origin_path)):
                os.makedirs(os.path.dirname(origin_path))
            self.info(
                f"Ln: Target {target_name}, Origin {origin_path}, Conf {conf_path}, Var {variant}"
            )
            self.run(
                f"ln {conf_path} {origin_path}",
                lambda: os.symlink(conf_path, origin_path),
            )

        if "post" in conf_config:
            post_cmd = self.render_with_env(conf_config["post"])
            self.run(f"run post action: {post_cmd}", lambda: os.system(post_cmd))

    def ln(self, permit_exec=False):
        """
        crepo ln ipset.conf
        crepo -t ipset ln ipset.conf
        crepo ln @ipset/ipset.conf
        crepo -t ipset -v raw ln ipset.conf
        """
        for conf_name in self.args.confs:
            target_name_from_path, conf_name = self.get_target_and_conf_name(conf_name)

            target_name = (
                self.args.target
                or target_name_from_path
                or ".".join(conf_name.split(".")[0:-1])
            )

            self.link_conf(target_name, conf_name, self.args.variant, permit_exec)

    def bk(self):
        """
        crepo bk iptables.rules
        crepo -t iptables -v ros -n my-iptables.rules bk iptables.rules
        crepo bk ~/.ssh/authorized_keys
        """
        for origin in self.args.origins:
            origin_path = os.path.abspath(origin)
            target_name = self.args.target or self.get_target_name_from_path(
                origin_path
            )
            if not target_name:
                self.error_exit("Target is not provided!", 4)

            target_dir = self.get_target_dir(target_name)

            # if not set name, use origin name, and strip leading dot
            conf_name = self.args.name or os.path.basename(origin_path).lstrip(".")
            conf_path = self.get_conf_path(target_name, conf_name, self.args.variant)

            self.info(
                f"Backup: Target {target_name}, Origin {origin_path}, Conf {conf_path}, Var {self.args.variant}"
            )

            if not (os.path.exists(target_dir) and os.path.isdir(target_dir)):
                self.run(f"mkdir {target_dir}", lambda: os.mkdir(target_dir))
                self.run(
                    f"chown {self.args.owner} {target_dir}",
                    lambda: self.chown(target_dir, self.args.owner),
                )

            self.run(
                f"cp {origin_path} {conf_path}",
                lambda: shutil.copyfile(origin_path, conf_path),
            )
            self.run(
                f"chown {self.args.owner} {conf_path}",
                lambda: self.chown(conf_path, self.args.owner),
            )
            self.run(f"rm {origin_path}", lambda: os.remove(origin_path))
            self.run(
                f"ln {conf_path} {origin_path}",
                lambda: os.symlink(conf_path, origin_path),
            )

            target_config = self.get_target_config(target_name)
            replaced_origin_path = self.replace_with_env(origin_path)
            if (
                conf_name in target_config
                and target_config[conf_name]["origin"] != replaced_origin_path
            ):
                self.error_exit("Origin conflicts", 5)

            target_config[conf_name] = {"origin": replaced_origin_path}
            self.run(
                f"save target config: {conf_name}=>{target_config[conf_name]}",
                lambda: self.save_target_config(target_name, target_config),
            )

    def install(self):
        """
        crepo install ipset
        crepo -v ros install ipset
        crepo install ipset:ros
        """
        for target_name in self.args.target_names:
            variant = self.args.variant
            if ":" in target_name:
                parts = target_name.split(":")
                target_name = parts[0]
                variant = ":".join(parts[1:])

            target_config = self.get_target_config(target_name)
            for conf_name in target_config:
                self.link_conf(
                    target_name, conf_name, variant, permit_exec=False, required=False
                )

    def unlink(self):
        """
        crepo restore ipset.conf
        """
        for origin in self.args.origins:
            conf_path = os.readlink(origin)
            self.run(f"rm {origin}", lambda: os.remove(origin))
            self.run(
                f"cp {conf_path} {origin}", lambda: shutil.copyfile(conf_path, origin)
            )

    def ls(self):
        pass

    def exec_conf(self, conf_path):
        if not os.access(conf_path, os.X_OK):
            self.error_exit(f"Conf file is not executable: {conf_path}", 6)
        p = subprocess.Popen(
            conf_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            env=self.env,
        )
        print(p.communicate()[0])

    def exec(self):
        self.ln(permit_exec=True)


def run_crepo(argv):
    parser = argparse.ArgumentParser(prog="crepo")
    parser.add_argument(
        "--repo-dir", default=(os.getenv("CREPO_ROOT") or "/.config-repo")
    )
    parser.add_argument("--root-dir", default="/")
    parser.add_argument("--user", default=os.getlogin())
    parser.add_argument("--user-home", default=os.path.join(os.path.expanduser("~")))

    parser.add_argument("--owner")

    parser.add_argument("-t", "--target")
    parser.add_argument("-v", "--variant")
    parser.add_argument("-n", "--name")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--silent", action="store_true")

    subparsers = parser.add_subparsers(dest="subcommand_name")

    parser_ln = subparsers.add_parser("ln")
    parser_ln.add_argument("confs", nargs="+")

    parser_bk = subparsers.add_parser("bk")
    parser_bk.add_argument("origins", nargs="+")

    parser_install = subparsers.add_parser("install")
    parser_install.add_argument("target_names", nargs="+")

    parser_unlink = subparsers.add_parser("unlink")
    parser_unlink.add_argument("origins", nargs="+")

    parser_unlink = subparsers.add_parser("ls")

    parser_exec = subparsers.add_parser("exec")
    parser_exec.add_argument("confs", nargs="+")

    args = parser.parse_args(argv)

    crepo = CRepo(args)
    if args.subcommand_name:
        getattr(crepo, args.subcommand_name)()
    else:
        parser.print_help()

    return crepo


def main():
    run_crepo(sys.argv[1:])


if __name__ == "__main__":
    main()
