import os
from base import BaseTestCase


class TestCreate(BaseTestCase):

    def test_create_10(self):
        crepo = self.run_default_crepo(
            f"create --type exec --default @fstab/newcreate.sh"
        )
        self.assertTrue(os.path.exists(self.repo("fstab/newcreate.sh")))
        self.assertTrue(os.access(self.repo("fstab/newcreate.sh"), os.X_OK))
        target_config = crepo.get_target_config("fstab")
        self.assertIn("newcreate.sh", target_config)
        self.assertEqual(target_config["newcreate.sh"]["type"], "exec")
        self.assertTrue(target_config["newcreate.sh"]["default"])

    def test_create_20(self):
        crepo = self.run_default_crepo(f"create @faketarget/ros:fake.conf")
        self.assertTrue(os.path.exists(self.repo("faketarget/ros:fake.conf")))

        target_config = crepo.get_target_config("faketarget")
        self.assertIn("fake.conf", target_config)

    def test_create_30(self):
        crepo = self.run_default_crepo(f"-v x create @faketarget/fake.conf")
        self.assertTrue(os.path.exists(self.repo("faketarget/x:fake.conf")))

        target_config = crepo.get_target_config("faketarget")
        self.assertIn("fake.conf", target_config)

    def test_create_40(self):
        self.run_default_crepo(
            f"create -F @ipset/raw:ipset.conf @faketarget/x:fake.conf"
        )
        self.assertFileEqual(
            self.repo("faketarget/x:fake.conf"),
            self.repo("ipset/raw:ipset.conf"),
        )
