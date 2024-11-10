import os
from ..crepo import CRepo
from .base import BaseCmd


class LsCmd(BaseCmd):

    def run(self, permit_exec=False):
        if self.args.path:
            target_name = self.crepo.remove_atsign_from_target_name(self.args.path)
            conf_names = self.crepo.get_target_config(target_name).keys()
            for file_name in sorted(
                os.listdir(self.crepo.get_target_path(target_name))
            ):
                conf_name = file_name
                if ":" in file_name:
                    conf_name, _ = self.crepo.get_conf_name_and_variant_from_path(
                        file_name
                    )

                if conf_name in conf_names:
                    self.crepo.info(f"@{target_name}/{file_name}")
        else:
            for target_name in sorted(os.listdir(self.crepo.args.repo_dir)):
                if os.path.exists(self.crepo.get_target_config_path(target_name)):
                    self.crepo.info(f"@{target_name}")
