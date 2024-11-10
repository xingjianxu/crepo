from ..crepo import CRepo
from .base import BaseCmd
from .path import get_file_path

class EditCmd(BaseCmd):

    def run(self, permit_exec=False):
        path = get_file_path(self.crepo)
        self.crepo.edit_file(path)
