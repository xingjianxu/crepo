import os
from test.base import BaseTestCase


class TestLn(BaseTestCase):
    def test_ln_1(self):
        self.run_default_crepo("-t ipset ln ipset.conf")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )

    def test_ln_2(self):
        self.run_default_crepo("ln ipset.conf"),
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )

    def test_ln_3(self):
        self.run_default_crepo("ln @ipset/ipset.conf")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )

    def test_ln_4(self):
        self.run_default_crepo("-v raw ln @ipset/ipset.conf")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf.raw",
        )

    def test_ln_5(self):
        self.run_default_crepo("ln @ipset/ipset.conf @ipset/a.conf")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )

    def test_ln_6(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("ln @ipset/x")
        self.assertEqual(cm.exception.code, 2)

    def test_ln_7(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("ln @ipset/not_in_config.conf")
        self.assertEqual(cm.exception.code, 3)

    def test_ln_8(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("-v x ln @ipset/ipset.conf")
        self.assertEqual(cm.exception.code, 2)

    def test_ln_9(self):
        self.run_default_crepo(f"ln @ssh/pkey")
        self.assertLn(
            f"/home/{self.user}/.ssh/id_rsa.pub",
            "ssh/pkey",
        )

    def test_ln_10(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("-t confilic_ipset ln @ipset/ipset.conf")
        self.assertEqual(cm.exception.code, 7)

    def test_ln_11(self):
        self.run_default_crepo(f"ln @ipset")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )

    def test_ln_12(self):
        self.run_default_crepo(f"ln @ssh")
        self.assertLn(
            f"/home/{self.user}/.ssh/id_rsa.pub",
            "ssh/pkey",
        )
