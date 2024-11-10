import os
import filecmp
from base import BaseTestCase


class TestGit(BaseTestCase):

    def setUp(self):
        os.environ["CREPO_HOME"] = os.path.join(
            os.path.dirname(__file__), os.path.pardir
        )

    def test_git_10(self):
        crepo = self.run_default_crepo("--dry-run git pull")
        self.assertListEqual(
            crepo.runner.runned_labels, [f"cd {self.repo()}", "git pull"]
        )

    def test_git_20(self):
        crepo = self.run_default_crepo("--dry-run git push")
        self.assertListEqual(
            crepo.runner.runned_labels,
            [f"cd {self.repo()}", f"git commit -a", "git push"],
        )

    def test_git_30(self):
        crepo = self.run_default_crepo("--dry-run git -s pull")
        self.assertListEqual(
            crepo.runner.runned_labels,
            [f"cd {os.getenv("CREPO_HOME")}", "git pull"],
        )

    def test_git_40(self):
        crepo = self.run_default_crepo("--dry-run git -s push")
        self.assertListEqual(
            crepo.runner.runned_labels,
            [f"cd {os.getenv("CREPO_HOME")}", f"git commit -a", "git push"],
        )
        print(crepo.runner.runned_labels)
