import unittest
import os
import pwd
import shutil
import json
from crepo import run_crepo

TEST_DIR = "/wrd/opt/crepo/testdata"


class TestCrepo(unittest.TestCase):

    crepo_etc = f"{TEST_DIR}/etc-tmp"
    crepo_root = f"{TEST_DIR}/repo-tmp"
    crepo_owner = "xingjian"

    default_args = [
        f"--repo-dir={crepo_root}",
        f"--owner={crepo_owner}",
        f"--etc-dir={crepo_etc}",
        "--silent",
    ]

    def assert_labels(self, crepo, labels):
        self.assertEqual(crepo.runner.runned_labels, labels)

    def assert_output(self, capfs, expected_output):
        cap = capfs.readouterr()
        self.assertEqual(cap.out, "\n".join(expected_output) + "\n")

    def run_default_crepo(self, cmd):
        return run_crepo(self.default_args + cmd.split())

    def setUp(self):
        shutil.copytree(f"{TEST_DIR}/repo", self.crepo_root)
        shutil.copytree(f"{TEST_DIR}/etc", self.crepo_etc)

    def tearDown(self):
        shutil.rmtree(self.crepo_root)
        shutil.rmtree(self.crepo_etc)

    def assertLn(self, link, conf):
        self.assertTrue(os.path.islink(link))
        self.assertEqual(os.readlink(link), conf)

    def test_ln_1(self):
        self.run_default_crepo("-t ipset ln ipset.conf")
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf",
        )

    def test_ln_2(self):
        self.run_default_crepo("ln ipset.conf"),
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf",
        )

    def test_ln_3(self):
        self.run_default_crepo("ln @ipset/ipset.conf")
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf",
        )

    def test_ln_4(self):
        self.run_default_crepo("-v raw ln @ipset/ipset.conf")
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf.raw",
        )

    def test_ln_5(self):
        self.run_default_crepo("ln @ipset/ipset.conf @ipset/a.conf")
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf",
        )

    def test_ln_6(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("ln @ipset/x")
        self.assertEqual(cm.exception.code, 2)

    def test_ln_7(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("-v x ln @ipset/ipset.conf")
        self.assertEqual(cm.exception.code, 2)

    def test_get_target_name_from_path_1(self):
        crepo = run_crepo(["ls"])
        self.assertEqual(
            crepo.get_target_name_from_path("/etc/xray/config.json"), "xray"
        )
        self.assertEqual(crepo.get_target_name_from_path("/etc/xray.json"), "xray")
        self.assertIsNone(crepo.get_target_name_from_path("/xray.json"))

    def test_get_target_name_from_path_2(self):
        crepo = self.run_default_crepo("ls")
        self.assertEqual(
            crepo.get_target_name_from_path(f"{self.crepo_etc}/xray/config.json"),
            "xray",
        )

    def assertBk(
        self, target_dir, conf_path, conf_size, origin_path, assert_target_config=None
    ):
        self.assertTrue(os.path.isdir(target_dir))
        self.assertEqual(
            pwd.getpwuid(os.stat(target_dir).st_uid).pw_name,
            self.crepo_owner,
        )
        self.assertEqual(os.path.getsize(conf_path), conf_size)
        self.assertEqual(
            pwd.getpwuid(os.stat(conf_path).st_uid).pw_name,
            self.crepo_owner,
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
        self.run_default_crepo(f"bk {self.crepo_etc}/iptables/iptables.rules")
        self.assertBk(
            f"{self.crepo_root}/iptables",
            f"{self.crepo_root}/iptables/iptables.rules",
            595,
            f"{self.crepo_etc}/iptables/iptables.rules",
        )

    def test_bk_2(self):
        self.run_default_crepo(
            f"-t iptables -v ros -n my-ip6tables.rules bk {self.crepo_etc}/iptables/ip6tables.rules"
        )

        def assert_target_config(target_config):
            self.assertIn("my-ip6tables.rules", target_config)
            self.assertEqual(
                target_config["my-ip6tables.rules"]["origin"],
                f"{{ETC}}/iptables/ip6tables.rules",
            )

        self.assertBk(
            f"{self.crepo_root}/iptables",
            f"{self.crepo_root}/iptables/my-ip6tables.rules.ros",
            105,
            f"{self.crepo_etc}/iptables/ip6tables.rules",
            assert_target_config,
        )

    def test_bk_3(self):
        self.run_default_crepo(
            f"-t systemd -n aaa.service bk {self.crepo_etc}/systemd/system/a.service"
        )

        def assert_target_config(target_config):
            self.assertIn("aaa.service", target_config)
            self.assertEqual(
                target_config["aaa.service"]["origin"],
                f"{{ETC}}/systemd/system/a.service",
            )

        self.assertBk(
            f"{self.crepo_root}/systemd",
            f"{self.crepo_root}/systemd/aaa.service",
            6,
            f"{self.crepo_etc}/systemd/system/a.service",
            assert_target_config,
        )

    def test_install_1(self):
        self.run_default_crepo(f"install ipset")
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf",
        )
        self.assertLn(
            f"{self.crepo_etc}/a.conf",
            f"{self.crepo_root}/ipset/a.conf",
        )

    def test_install_2(self):
        self.run_default_crepo(f"-v notfound install ipset")
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf",
        )
        self.assertLn(
            f"{self.crepo_etc}/a.conf",
            f"{self.crepo_root}/ipset/a.conf",
        )
        self.assertFalse(os.path.exists(f"/b.conf"))

    def test_install_3(self):
        self.run_default_crepo(f"-v raw install ipset")
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf.raw",
        )
        self.assertLn(
            f"{self.crepo_etc}/a.conf",
            f"{self.crepo_root}/ipset/a.conf",
        )
        self.assertLn(
            f"{self.crepo_etc}/b.conf",
            f"{self.crepo_root}/ipset/b.conf.raw",
        )

    def test_install_4(self):
        self.run_default_crepo(f"install ipset sysctl")
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf",
        )
        self.assertLn(
            f"{self.crepo_etc}/a.conf",
            f"{self.crepo_root}/ipset/a.conf",
        )
        self.assertLn(
            f"{self.crepo_etc}/sysctl.d/30-net.conf",
            f"{self.crepo_root}/sysctl/net.conf",
        )

    def test_install_5(self):
        self.run_default_crepo(f"install ipset:raw sysctl")
        self.assertLn(
            f"{self.crepo_etc}/ipset.conf",
            f"{self.crepo_root}/ipset/ipset.conf.raw",
        )
        self.assertLn(
            f"{self.crepo_etc}/a.conf",
            f"{self.crepo_root}/ipset/a.conf",
        )
        self.assertLn(
            f"{self.crepo_etc}/b.conf",
            f"{self.crepo_root}/ipset/b.conf.raw",
        )
        self.assertLn(
            f"{self.crepo_etc}/sysctl.d/30-net.conf",
            f"{self.crepo_root}/sysctl/net.conf",
        )


if __name__ == "__main__":
    unittest.main()
