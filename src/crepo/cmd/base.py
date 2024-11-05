import abc
from crepo.crepo import CRepo


class BaseCmd:
    __metaclass__ = abc.ABCMeta

    def __init__(self, crepo: CRepo, args):
        self.crepo = crepo
        self.args = args

    @abc.abstractmethod
    def run(self, permit_exec=False):
        return
