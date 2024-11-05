import os
import shutil
from ..crepo import CRepo
from .base import BaseCmd


class BkCmd(BaseCmd):
    def run(self, permit_exec=False):
        """
        crepo bk iptables.rules
        crepo -t iptables -v ros -n my-iptables.rules bk iptables.rules
        crepo bk ~/.ssh/authorized_keys
        """
        for origin in self.args.origins:
            origin_path = os.path.abspath(origin)
            target_name = self.args.target or self.crepo.get_target_name_from_path(
                origin_path
            )
            if not target_name:
                self.crepo.error_exit("Target is not provided!", 4)

            target_dir = self.crepo.get_target_dir(target_name)

            # if not set name, use origin name, and strip leading dot
            conf_name = self.args.name or os.path.basename(origin_path).lstrip(".")
            conf_path = self.crepo.get_conf_path(
                target_name, conf_name, self.args.variant
            )

            self.crepo.info(
                f"Backup: Target {target_name}, Origin {origin_path}, Conf {conf_path}, Var {self.args.variant}"
            )

            self.crepo.mk_target_dir(target_dir)

            self.crepo.run(
                f"cp {origin_path} {conf_path}",
                lambda: shutil.copyfile(origin_path, conf_path),
            )
            self.crepo.run(
                f"chown {self.args.owner} {conf_path}",
                lambda: self.crepo.chown(conf_path, self.args.owner),
            )
            self.crepo.run(f"rm {origin_path}", lambda: os.remove(origin_path))
            self.crepo.run(
                f"ln {conf_path} {origin_path}",
                lambda: os.symlink(conf_path, origin_path),
            )

            target_config = self.crepo.get_target_config(target_name)
            replaced_origin_path = self.crepo.replace_with_env(origin_path)
            if (
                conf_name in target_config
                and target_config[conf_name]["origin"] != replaced_origin_path
            ):
                self.crepo.error_exit("Origin conflicts", 5)

            target_config[conf_name] = {"origin": replaced_origin_path}
            self.crepo.run(
                f"save target config: {conf_name}=>{target_config[conf_name]}",
                lambda: self.crepo.save_target_config(target_name, target_config),
            )
