import os
from base import BaseTestCase


class TestInstall(BaseTestCase):
    def test_install_1(self):
        self.run_default_crepo(f"install ipset")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )
        self.assertLn(
            "etc/a.conf",
            "ipset/a.conf",
        )

    def test_install_2(self):
        self.run_default_crepo(f"-v notfound install ipset")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )
        self.assertLn(
            "etc/a.conf",
            "ipset/a.conf",
        )
        self.assertFalse(os.path.exists(self.root("etc/b.conf")))

    def test_install_3(self):
        self.run_default_crepo(f"-v raw install ipset")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf.raw",
        )
        self.assertLn(
            "etc/a.conf",
            "ipset/a.conf",
        )
        self.assertLn(
            "etc/b.conf",
            "ipset/b.conf.raw",
        )

    def test_install_4(self):
        self.run_default_crepo(f"install ipset sysctl")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )
        self.assertLn(
            "etc/a.conf",
            "ipset/a.conf",
        )
        self.assertLn(
            "etc/sysctl.d/30-net.conf",
            "sysctl/net.conf",
        )

    def test_install_5(self):
        self.run_default_crepo(f"install ipset:raw sysctl")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf.raw",
        )
        self.assertLn(
            "etc/a.conf",
            "ipset/a.conf",
        )
        self.assertLn(
            "etc/b.conf",
            "ipset/b.conf.raw",
        )
        self.assertLn(
            "etc/sysctl.d/30-net.conf",
            "sysctl/net.conf",
        )
