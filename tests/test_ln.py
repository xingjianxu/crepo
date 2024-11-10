from base import BaseTestCase


class TestLn(BaseTestCase):

    def test_ln_00(self):
        self.run_default_crepo("-t ipset ln ipset.conf")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )

    def test_ln_01(self):
        self.run_default_crepo("-t ipset ln ipset.conf")
        # ln again in strict mode should raise error
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("-S -t ipset ln ipset.conf")

        from crepo.crepo import ERROR_ORIGIN_EXISTS

        self.assertEqual(cm.exception.code, ERROR_ORIGIN_EXISTS)

    def test_ln_02(self):
        self.run_default_crepo("-t ipset ln ipset.conf")
        # ln again in non strict mode should not raise error
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
            "ipset/raw:ipset.conf",
        )

    def test_ln_5(self):
        self.run_default_crepo("ln @ipset/ipset.conf @ipset/a.conf")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )

    def test_ln_60(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("ln @ipset/x")
        self.assertEqual(cm.exception.code, 3)

    def test_ln_61(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("-S ln @ipset/x")
        self.assertEqual(cm.exception.code, 2)

    def test_ln_7(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("ln @ipset/not_in_config.conf")
        self.assertEqual(cm.exception.code, 3)

    def test_ln_80(self):
        with self.assertRaises(SystemExit) as cm:
            self.run_default_crepo("-S -v x ln @ipset/ipset.conf")
        self.assertEqual(cm.exception.code, 2)

    def test_ln_81(self):
        self.run_default_crepo("-v x ln @ipset/ipset.conf")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/ipset.conf",
        )

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

    def test_ln_13(self):
        self.run_default_crepo("ln @ipset/raw:ipset.conf")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/raw:ipset.conf",
        )

    def test_ln_14(self):
        self.run_default_crepo("-v raw ln @ipset/ipset.conf")
        self.assertLn(
            "etc/ipset.conf",
            "ipset/raw:ipset.conf",
        )
