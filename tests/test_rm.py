import os
import filecmp
from unittest.mock import patch
from base import BaseTestCase


class TestRm(BaseTestCase):

    def test_rm_1(self):
        crepo = self.run_default_crepo(f"rm @ipset/ipset.conf")
        self.assertFalse(
            os.path.exists(self.repo("ipset/ipset.conf")),
        )
        self.assertIn("ipset.conf", crepo.get_target_config("ipset"))

    def test_rm_2(self):
        crepo = self.run_default_crepo(f"rm @ipset")
        self.assertFalse(
            os.path.exists(self.repo("ipset")),
        )

    def test_rm_3(self):
        crepo = self.run_default_crepo(f"-t ipset rm")
        self.assertFalse(
            os.path.exists(self.repo("ipset")),
        )

    def test_rm_4(self):
        crepo = self.run_default_crepo(f"rm @ipset/raw:ipset.conf")
        self.assertFalse(
            os.path.exists(self.repo("ipset/raw:ipset.conf")),
        )
        self.assertIn("ipset.conf", crepo.get_target_config("ipset"))

    def test_rm_5(self):
        crepo = self.run_default_crepo(f"-t ipset -v raw rm")
        self.assertFalse(
            os.path.exists(self.repo("ipset/raw:ipset.conf")),
        )
        self.assertFalse(
            os.path.exists(self.repo("ipset/raw:b.conf")),
        )

    def test_rm_6(self):
        crepo = self.run_default_crepo(f"rm @ipset/raw:")
        self.assertFalse(
            os.path.exists(self.repo("ipset/raw:ipset.conf")),
        )
        self.assertFalse(
            os.path.exists(self.repo("ipset/raw:b.conf")),
        )

    def test_rm_7(self):
        self.run_default_crepo("-t ipset ln ipset.conf")
        crepo = self.run_default_crepo(f"rm {self.root('/etc/ipset.conf')}")
