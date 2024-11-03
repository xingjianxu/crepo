import os
from test_crepo import TestCRepo


class TestLn(TestCRepo):
    def test_ln_1(self):
        self.run_default_crepo("-t ipset ln ipset.conf")
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf"),
        )

    def test_ln_2(self):
        self.run_default_crepo("ln ipset.conf"),
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf"),
        )

    def test_ln_3(self):
        self.run_default_crepo("ln @ipset/ipset.conf")
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf"),
        )

    def test_ln_4(self):
        self.run_default_crepo("-v raw ln @ipset/ipset.conf")
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf.raw"),
        )

    def test_ln_5(self):
        self.run_default_crepo("ln @ipset/ipset.conf @ipset/a.conf")
        self.assertLn(
            self.root("etc/ipset.conf"),
            self.repo("ipset/ipset.conf"),
        )

    def test_ln_6(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("ln @ipset/x")
        self.assertEqual(cm.exception.code, 2)

    def test_ln_7(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("-v x ln @ipset/ipset.conf")
        self.assertEqual(cm.exception.code, 2)
