from ..crepo import CRepo
from .base import BaseCmd


class EditCmd(BaseCmd):

    def run(self, permit_exec=False):
        target_name, conf_name, variant = self.crepo.parse_path(self.args.conf)
        conf_path = self.crepo.get_conf_path(target_name, conf_name, variant)
        self.crepo.edit_file(conf_path)
