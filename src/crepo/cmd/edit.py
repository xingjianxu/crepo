from ..crepo import CRepo
from .base import BaseCmd


class EditCmd(BaseCmd):

    def run(self, permit_exec=False):
        path = None
        if self.args.target_config:
            target_name = (
                self.args.conf[1:] if self.args.conf.startswith("@") else self.args.conf
            )
            path = self.crepo.get_target_config_path(target_name)
        else:
            target_name, conf_name, variant = self.crepo.parse_path(self.args.conf)
            path = self.crepo.get_conf_path(target_name, conf_name, variant)
        self.crepo.edit_file(path)
