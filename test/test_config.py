import os
from io import StringIO
from unittest.mock import patch
from test.base import BaseTestCase


class TestConfig(BaseTestCase):

    def test_config(self):
        self.run_default_crepo(f"config --type exec --default @fstab/created.sh")
