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
        self.assertLabels(crepo, [f"cd {self.repo()}", "git pull"])

    def test_git_20(self):
        crepo = self.run_default_crepo("--dry-run git push")
        self.assertLabels(
            crepo,
            [f"cd {self.repo()}", "git add --all", "git commit", "git push"],
        )

    def test_git_30(self):
        crepo = self.run_default_crepo("--dry-run git -s pull")
        self.assertLabels(
            crepo,
            [f"cd {os.getenv("CREPO_HOME")}", "git pull"],
        )

    def test_git_40(self):
        crepo = self.run_default_crepo("--dry-run git -s push")
        self.assertLabels(
            crepo,
            [
                f"cd {os.getenv("CREPO_HOME")}",
                "git add --all",
                "git commit",
                "git push",
            ],
        )
