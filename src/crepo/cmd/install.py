from ..crepo import CRepo
from .base import BaseCmd


class InstallCmd(BaseCmd):
    def run(self, permit_exec=False):
        """
        crepo install ipset
        crepo -v ros install ipset
        crepo install ipset:ros
        """
        for target_name in self.args.target_names:
            variant = self.args.variant
            if ":" in target_name:
                parts = target_name.split(":")
                target_name = parts[0]
                variant = ":".join(parts[1:])

            target_config = self.crepo.get_target_config(target_name)
            for conf_name in target_config:
                self.crepo.link_conf(
                    target_name, conf_name, variant, permit_exec=False, required=False
                )
