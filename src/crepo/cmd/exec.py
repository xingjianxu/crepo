from ..crepo import CRepo
from .base import BaseCmd
from .ln import LnCmd


class ExecCmd(LnCmd):
    def __init__(self, crepo: CRepo, args):
        self.crepo = crepo
        self.args = args

    def run(self, permit_exec=False):
        super().run(permit_exec=True)
