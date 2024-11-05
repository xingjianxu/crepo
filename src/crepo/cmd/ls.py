from ..crepo import CRepo
from .base import BaseCmd


class LsCmd(BaseCmd):
    def __init__(self, crepo: CRepo, args):
        self.crepo = crepo
        self.args = args

    def run(self, permit_exec=False):
        pass
