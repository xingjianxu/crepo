import os
import shutil
from ..crepo import CRepo
from .base import BaseCmd


class UnlinkCmd(BaseCmd):

    def run(self, permit_exec=False):
        """
        crepo restore ipset.conf
        """
        for origin in self.args.origins:
            conf_path = os.readlink(origin)
            self.crepo.run(f"rm {origin}", lambda: os.remove(origin))
            self.crepo.run(
                f"cp {conf_path} {origin}", lambda: shutil.copyfile(conf_path, origin)
            )
