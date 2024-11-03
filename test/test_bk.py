import os
import pwd
import json
import filecmp
from test_crepo import TestCRepo


class TestBk(TestCRepo):

    def assertBk(self, crepo, **params):
        target_name = params["target_name"]
        target_dir = self.repo(target_name)

        conf_name = params["conf_name"]
        conf_path = crepo.get_conf_path(
            target_name, conf_name, variant=params.get("variant")
        )

        origin_path = self.root(params.get("origin_path"))

        self.assertTrue(os.path.isdir(target_dir))
        self.assertEqual(
            pwd.getpwuid(os.stat(target_dir).st_uid).pw_name,
            self.owner,
        )
        self.assertTrue(
            filecmp.cmp(conf_path, os.path.join(self.test_data_root_dir, origin_path))
        )

        self.assertEqual(
            pwd.getpwuid(os.stat(conf_path).st_uid).pw_name,
            self.owner,
        )
        self.assertTrue(os.path.islink(origin_path))

        self.assertEqual(
            os.readlink(origin_path),
            conf_path,
        )
        target_config_path = f"{target_dir}/.target.json"
        self.assertTrue(
            os.path.isfile(target_config_path),
            f"target config not found: {target_config_path}",
        )
        with open(target_config_path, "r") as file:
            target_config = json.load(file)
            self.assertIn(conf_name, target_config)
            self.assertEqual(
                target_config[conf_name]["origin"],
                params.get("origin_path_in_config") or origin_path,
                "target config origin path error",
            )
            if "assert_target_config" in params:
                params["assert_target_config"](target_config)

    def test_bk_1(self):
        crepo = self.run_default_crepo(
            f"bk {self.root("/etc/iptables/iptables.rules")}"
        )
        self.assertBk(
            crepo,
            target_name="iptables",
            conf_name="iptables.rules",
            origin_path="/etc/iptables/iptables.rules",
            origin_path_in_config="{ETC}/iptables/iptables.rules",
        )

    def test_bk_2(self):
        crepo = self.run_default_crepo(
            f"-t iptables -v ros -n my-ip6tables.rules bk {self.root('etc/iptables/ip6tables.rules')}"
        )

        self.assertBk(
            crepo,
            target_name="iptables",
            conf_name="my-ip6tables.rules",
            variant="ros",
            origin_path="/etc/iptables/ip6tables.rules",
            origin_path_in_config="{ETC}/iptables/ip6tables.rules",
        )

    def test_bk_3(self):
        crepo = self.run_default_crepo(
            f"-t systemd -n aaa.service bk {self.root('/etc/systemd/system/a.service')}"
        )

        self.assertBk(
            crepo,
            target_name="systemd",
            conf_name="aaa.service",
            origin_path="/etc/systemd/system/a.service",
            origin_path_in_config="{ETC}/systemd/system/a.service",
        )

    def test_bk_4(self):
        home_dir = "/home/tu"
        crepo = self.run_default_crepo(f"bk {self.root(f'{home_dir}/.ssh/id_rsa')}")

        self.assertBk(
            crepo,
            target_name="ssh",
            conf_name="id_rsa",
            origin_path=f"{home_dir}/.ssh/id_rsa",
            origin_path_in_config="{USER_HOME}/.ssh/id_rsa",
        )

    def test_bk_5(self):
        home_dir = "/home/tu"
        crepo = self.run_default_crepo(
            f"bk {self.root(f'{home_dir}/.config/htop/htoprc')}"
        )

        self.assertBk(
            crepo,
            target_name="htop",
            conf_name="htoprc",
            origin_path=f"{home_dir}/.config/htop/htoprc",
            origin_path_in_config="{USER_HOME}/.config/htop/htoprc",
        )

    def test_bk_6(self):
        home_dir = "/home/tu"
        crepo = self.run_default_crepo(f"bk {self.root(f'{home_dir}/.zshrc')}")

        self.assertBk(
            crepo,
            target_name="zsh",
            conf_name="zshrc",
            origin_path=f"{home_dir}/.zshrc",
            origin_path_in_config="{USER_HOME}/.zshrc",
        )

    def test_bk_7(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("bk @not_exist_target/d")
        self.assertEqual(cm.exception.code, 4)
