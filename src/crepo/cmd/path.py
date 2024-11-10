from ..crepo import CRepo
from .base import BaseCmd


def get_file_path(crepo):
    path = None
    if crepo.args.target_config:
        target_name = (
            crepo.args.conf[1:] if crepo.args.conf.startswith("@") else crepo.args.conf
        )
        path = crepo.get_target_config_path(target_name)
    else:
        target_name, conf_name, variant = crepo.parse_path(crepo.args.conf)
        path = crepo.get_conf_path(target_name, conf_name, variant)
    return path


class PathCmd(BaseCmd):

    def run(self, permit_exec=False):
        path = get_file_path(self.crepo)
        self.crepo.info(path)
