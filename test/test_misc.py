from test_crepo import TestCRepo
from crepo import run_crepo


class TestMisc(TestCRepo):
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
            crepo.get_target_name_from_path(self.root("etc/xray/config.json")),
            "xray",
        )
