import os
from io import StringIO
from unittest.mock import patch
from test.base import BaseTestCase


class TestCreate(BaseTestCase):

    def test_create(self):
        crepo = self.run_default_crepo(f"create --type exec @fstab/created.sh")
        self.assertTrue(os.path.exists(self.repo("fstab/created.sh")))
        self.assertEqual(os.access(self.repo("fstab/created.sh"), os.X_OK))
