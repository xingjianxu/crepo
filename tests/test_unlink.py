import os
import filecmp
from unittest.mock import patch
from base import BaseTestCase


class TestUnlink(BaseTestCase):

    def test_unlink(self):
        self.run_default_crepo("-t ipset ln ipset.conf")
        origin_path = "/etc/ipset.conf"
        crepo = self.run_default_crepo(f"unlink {self.root(origin_path)}")
        conf_path = crepo.get_conf_path(
            "ipset",
            "ipset.conf",
        )
        self.assertTrue(
            filecmp.cmp(conf_path, os.path.join(self.test_data_root_dir, origin_path))
        )
