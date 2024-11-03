import unittest
import os
import sys
import shutil
import tempfile

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, os.pardir)
sys.path.append(parent_dir)

from crepo import run_crepo


class TestCRepo(unittest.TestCase):

    PREPARED_DATA_DIR_NAMES = ["root", "repo"]

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        self.test_data_root_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data"
        )
        self.test_data_tmp_dir = tempfile.TemporaryDirectory().name
        self.owner = "xingjian"
        self.root_dir = os.path.join(self.test_data_tmp_dir, "root")
        self.repo_dir = os.path.join(self.test_data_tmp_dir, "repo")
        self.default_args = [
            f"--repo-dir={self.repo_dir}",
            f"--owner={self.owner}",
            f"--root-dir={self.root_dir}",
            "--silent",
        ]

    def root(self, path):
        return os.path.join(self.root_dir, path)

    def repo(self, path):
        return os.path.join(self.repo_dir, path)

    def run_default_crepo(self, cmd):
        return run_crepo(self.default_args + cmd.split())

    def assertLn(self, link, conf):
        self.assertTrue(os.path.islink(link))
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
        for data_dir in self.PREPARED_DATA_DIR_NAMES:
            shutil.rmtree(os.path.join(self.test_data_tmp_dir, data_dir))
