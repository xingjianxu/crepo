import os
from io import StringIO
from unittest.mock import patch
from test.base import BaseTestCase


class TestExec(BaseTestCase):
    def test_exec_1(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.run_default_crepo(f"exec @fstab/fstab.sh")
            self.assertEqual(
                fake_out.getvalue(), "b'This is a test file for fstab\\n'\n"
            )

    def test_exec_2(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            crepo = self.run_default_crepo(f"exec @fstab/printenv.sh")
            self.assertEqual(
                fake_out.getvalue(),
                f"b'{crepo.args.user_home}\\n{crepo.etc_dir}\\nfstab\\n{self.repo('fstab/printenv.sh')}\\n'\n",
            )
