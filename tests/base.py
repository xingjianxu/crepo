import unittest
import os
import sys
import shutil
import tempfile

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, os.pardir, "src")
sys.path.append(src_dir)

from crepo.crepo import run_crepo


class BaseTestCase(unittest.TestCase):

    PREPARED_DATA_DIR_NAMES = ["root", "repo"]

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        self.test_data_root_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data"
        )
        self.test_data_tmp_dir_obj = tempfile.TemporaryDirectory()
        self.test_data_tmp_dir = self.test_data_tmp_dir_obj.name
        self.owner = "xingjian"
        self.root_dir = os.path.join(self.test_data_tmp_dir, "root")
        self.repo_dir = os.path.join(self.test_data_tmp_dir, "repo")
        self.user = "tu"
        self.user_home = self.root("home", self.user)
        self.default_args = [
            f"--repo-dir={self.repo_dir}",
            f"--owner={self.owner}",
            f"--root-dir={self.root_dir}",
            f"--user={self.user}",
            f"--user-home={self.user_home}",
            "--silent",
        ]

    def root(self, *paths):
        return os.path.join(
            self.root_dir,
            *(path[1:] if path.startswith("/") else path for path in paths),
        )

    def repo(self, *paths):
        return os.path.join(
            self.repo_dir,
            *(path[1:] if path.startswith("/") else path for path in paths),
        )

    def run_default_crepo(self, cmd):
        return run_crepo(self.default_args + cmd.split())

    def assertLn(self, link, conf):
        link = self.root(link)
        conf = self.repo(conf)
        self.assertTrue(os.path.islink(link), f"Link not found: {link}")
        self.assertEqual(os.readlink(link), conf)

    def assert_labels(self, crepo, labels):
        self.assertEqual(crepo.runner.runned_labels, labels)

    def assert_output(self, capfs, expected_output):
        cap = capfs.readouterr()
        self.assertEqual(cap.out, "\n".join(expected_output) + "\n")

    def setUp(self):
        for data_dir in self.PREPARED_DATA_DIR_NAMES:
            shutil.copytree(
                os.path.join(self.test_data_root_dir, data_dir),
                os.path.join(self.test_data_tmp_dir, data_dir),
            )

    def tearDown(self):
        self.test_data_tmp_dir_obj.cleanup()
