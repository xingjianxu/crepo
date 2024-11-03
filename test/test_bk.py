import os
import pwd
import json
from test_crepo import TestCRepo


class TestBk(TestCRepo):
    def assertBk(
        self, target_dir, conf_path, conf_size, origin_path, assert_target_config=None
    ):
        self.assertTrue(os.path.isdir(target_dir))
        self.assertEqual(
            pwd.getpwuid(os.stat(target_dir).st_uid).pw_name,
            self.owner,
        )
        self.assertEqual(os.path.getsize(conf_path), conf_size)
        self.assertEqual(
            pwd.getpwuid(os.stat(conf_path).st_uid).pw_name,
            self.owner,
        )
        self.assertTrue(origin_path)
        self.assertEqual(
            os.readlink(origin_path),
            conf_path,
        )
        target_config_path = f"{target_dir}/.target.json"
        self.assertTrue(os.path.isfile(target_config_path))
        if assert_target_config:
            with open(target_config_path, "r") as file:
                assert_target_config(json.load(file))

    def test_bk_1(self):
        self.run_default_crepo(f"bk {self.root("etc/iptables/iptables.rules")}")
        self.assertBk(
            self.repo("iptables"),
            self.repo("iptables/iptables.rules"),
            595,
            self.root("etc/iptables/iptables.rules"),
        )

    def test_bk_2(self):
        self.run_default_crepo(
            f"-t iptables -v ros -n my-ip6tables.rules bk {self.root('etc/iptables/ip6tables.rules')}"
        )

        def assert_target_config(target_config):
            self.assertIn("my-ip6tables.rules", target_config)
            self.assertEqual(
                target_config["my-ip6tables.rules"]["origin"],
                f"{{ETC}}/iptables/ip6tables.rules",
            )

        self.assertBk(
            self.repo("iptables"),
            self.repo("iptables/my-ip6tables.rules.ros"),
            105,
            self.root("etc/iptables/ip6tables.rules"),
            assert_target_config,
        )

    def test_bk_3(self):
        self.run_default_crepo(
            f"-t systemd -n aaa.service bk {self.root('etc/systemd/system/a.service')}"
        )

        def assert_target_config(target_config):
            self.assertIn("aaa.service", target_config)
            self.assertEqual(
                target_config["aaa.service"]["origin"],
                f"{{ETC}}/systemd/system/a.service",
            )

        self.assertBk(
            self.repo("systemd"),
            self.repo("systemd/aaa.service"),
            6,
            self.root("etc/systemd/system/a.service"),
            assert_target_config,
        )
