import os
import stat
import shutil
from ..crepo import CRepo
from .base import BaseCmd


class CreateCmd(BaseCmd):
    def run(self, permit_exec=False):
        for conf_name in self.args.confs:
            target_name, conf_name, variant = self.crepo.parse_path(conf_name)
            self.crepo.info(f"Create: Target {target_name}, Conf {conf_name}")
            self.crepo.mk_target_dir(self.crepo.get_target_path(target_name))

            conf_path = self.crepo.get_conf_path(target_name, conf_name, variant)

            if self.args.from_template:
                t_target_name, t_conf_name, t_variant = self.crepo.parse_path(
                    self.args.from_template
                )
                t_conf_path = self.crepo.get_conf_path(
                    t_target_name, t_conf_name, t_variant
                )
                shutil.copyfile(t_conf_path, conf_path)
            else:
                with open(conf_path, "w") as file:
                    file.write("")

            if self.args.type == "exec":
                st = os.stat(conf_path)
                self.crepo.run(
                    f"chmod +x {conf_path}",
                    lambda: os.chmod(conf_path, st.st_mode | stat.S_IEXEC),
                )
            self.crepo.save_target_config(
                target_name,
                {conf_name: {"type": self.args.type, "default": self.args.default}},
            )

            if self.args.edit:
                self.crepo.edit_file(conf_path)
