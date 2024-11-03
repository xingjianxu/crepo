import os
from test_crepo import TestCRepo


class TestInstall(TestCRepo):
    def test_install_1(self):
        self.run_default_crepo(f"install ipset")
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf"),
        )
        self.assertLn(
            self.root("etc/a.conf"),
            self.repo("ipset/a.conf"),
        )

    def test_install_2(self):
        self.run_default_crepo(f"-v notfound install ipset")
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf"),
        )
        self.assertLn(
            self.root("etc/a.conf"),
            self.repo("ipset/a.conf"),
        )
        self.assertFalse(os.path.exists(self.root("etc/b.conf")))

    def test_install_3(self):
        self.run_default_crepo(f"-v raw install ipset")
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf.raw"),
        )
        self.assertLn(
            self.root("etc/a.conf"),
            self.repo("ipset/a.conf"),
        )
        self.assertLn(
            self.root("etc/b.conf"),
            self.repo("ipset/b.conf.raw"),
        )

    def test_install_4(self):
        self.run_default_crepo(f"install ipset sysctl")
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf"),
        )
        self.assertLn(
            self.root("etc/a.conf"),
            self.repo("ipset/a.conf"),
        )
        self.assertLn(
            self.root("etc/sysctl.d/30-net.conf"),
            self.repo("sysctl/net.conf"),
        )

    def test_install_5(self):
        self.run_default_crepo(f"install ipset:raw sysctl")
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf.raw"),
        )
        self.assertLn(
            self.root("etc/a.conf"),
            self.repo("ipset/a.conf"),
        )
        self.assertLn(
            self.root("etc/b.conf"),
            self.repo("ipset/b.conf.raw"),
        )
        self.assertLn(
            self.root("etc/sysctl.d/30-net.conf"),
            self.repo("sysctl/net.conf"),
        )
