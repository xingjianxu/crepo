import os
import stat
from ..crepo import CRepo
from .base import BaseCmd


class CreateCmd(BaseCmd):
    def run(self, permit_exec=False):
        for conf_name in self.args.confs:
            target_name, conf_name, variant = self.crepo.parse_path(conf_name)
            self.crepo.info(f"Create: Target {target_name}, Conf {conf_name}")
            self.crepo.mk_target_dir(self.crepo.get_target_path(target_name))
            conf_path = self.crepo.get_conf_path(target_name, conf_name, variant)
            with open(conf_path, "w") as file:
                file.write("")
            st = os.stat(conf_path)
            os.chmod(conf_path, st.st_mode | stat.S_IEXEC)
            print(f"Created: {self.args.default}")
            self.crepo.save_target_config(
                target_name,
                {conf_name: {"type": self.args.type, "default": self.args.default}},
            )
