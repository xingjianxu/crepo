import os
from ..crepo import CRepo
from .base import BaseCmd


class GitCmd(BaseCmd):

    def run(self, permit_exec=False):
        """
        crepo update
        """
        pwd = os.getenv("CREPO_HOME") if self.args.self else self.args.repo_dir
        self.crepo.run(f"cd {pwd}", lambda: os.chdir(pwd))
        if self.args.action == "pull":
            self.crepo.info(f"Pulling changes from remote: {pwd}")
            self.crepo.run(f"git pull", lambda: os.system("git pull"))
        elif self.args.action == "push":
            self.crepo.info(f"Committing and Pushing changes to remote: {pwd}")

            self.crepo.run(
                "git add --all",
                lambda: os.system("git add --all"),
            )

            self.crepo.run(
                "git commit",
                lambda: os.system("git commit"),
            )
            self.crepo.run(f"git push", lambda: os.system("git push"))
