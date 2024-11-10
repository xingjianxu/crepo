from io import StringIO
from unittest.mock import patch
from base import BaseTestCase


class TestLs(BaseTestCase):

    def test_ls_01(self):
        self.run_default_crepo("ls @ipset")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            crepo = self.run_default_crepo(f"ls @ipset")
