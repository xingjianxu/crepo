import os
from base import BaseTestCase
from crepo.crepo import run_crepo


class TestMisc(BaseTestCase):
    def test_get_target_name_from_path_1(self):
        crepo = run_crepo(["--silent", "ls"])
        self.assertEqual(
            crepo.get_target_name_from_path("/etc/xray/config.json"), "xray"
        )
        self.assertEqual(crepo.get_target_name_from_path("/etc/xray.json"), "xray")
        self.assertIsNone(crepo.get_target_name_from_path("/xray.json"))

    def test_get_target_name_from_path_2(self):
        crepo = self.run_default_crepo("ls")
        self.assertEqual(
            crepo.get_target_name_from_path(self.root("/etc/xray/config.json")),
            "xray",
        )

    def test_get_target_name_from_path_3(self):
        crepo = run_crepo(["--silent", "ls"])
        self.assertEqual(crepo.get_target_name_from_path("/home/tu/.ssh/id_rsa"), "ssh")

    def test_get_target_name_from_path_4(self):
        crepo = run_crepo(["--silent", "ls"])
        self.assertEqual(
            crepo.get_target_name_from_path("/home/tu/.config/htop/htoprc"), "htop"
        )

    def test_get_target_name_from_path_5(self):
        crepo = run_crepo(["--silent", "ls"])
        self.assertEqual(
            crepo.get_target_name_from_path("/home/tu/.config/.test.json"), "test"
        )

    def test_get_target_name_from_path_6(self):
        crepo = run_crepo(["--silent", "ls"])
        self.assertEqual(crepo.get_target_name_from_path("/home/tu/.zshrc"), "zsh")

    def test_get_conf_variants_1(self):
        crepo = self.run_default_crepo("ls")
        self.assertListEqual(
            crepo.get_conf_variant_paths("ipset", "ipset.conf"),
            ["ipset.conf", "raw:ipset.conf"],
        )

    def test_get_conf_variants_2(self):
        crepo = self.run_default_crepo("ls")
        self.assertListEqual(
            crepo.get_conf_variant_paths("ipset", "i"),
            [],
        )

    def test_default_args_1(self):
        import socket

        crepo = run_crepo(["--silent", "ls"])
        self.assertEqual(crepo.args.variant, socket.gethostname())

        VARIANT = "SPECIAL_VARIANT"
        os.environ["CREPO_VARIANT"] = VARIANT
        crepo = run_crepo(["--silent", "ls"])
        self.assertEqual(crepo.args.variant, VARIANT)

        crepo = run_crepo(["--silent", "-D", "ls"])
        self.assertIsNone(crepo.args.variant)
