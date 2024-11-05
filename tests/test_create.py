import os
from io import StringIO
from unittest.mock import patch
from base import BaseTestCase


class TestCreate(BaseTestCase):

    def test_create_1(self):
        crepo = self.run_default_crepo(
            f"create --type exec --default @fstab/newcreate.sh"
        )
        self.assertTrue(os.path.exists(self.repo("fstab/newcreate.sh")))
        self.assertTrue(os.access(self.repo("fstab/newcreate.sh"), os.X_OK))
        target_config = crepo.get_target_config("fstab")
        self.assertIn("newcreate.sh", target_config)
        self.assertEqual(target_config["newcreate.sh"]["type"], "exec")
        self.assertTrue(target_config["newcreate.sh"]["default"])
