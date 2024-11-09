import os
import shutil
from ..crepo import CRepo
from .base import BaseCmd


class RmCmd(BaseCmd):

    def run(self, permit_exec=False):
        """
        crepo rm @ipset/ipset.conf
        crepo rm @ipset
        crepo rm @ipset/raw:
        """
        if len(self.args.confs) == 0 and self.args.target:
            self.rm(self.args.target, None, self.args.variant)

        for conf in self.args.confs:
            if os.path.islink(conf):
                conf_path = os.readlink(conf)
                self.crepo.run(f"rm {conf}", lambda: os.remove(conf))
                self.crepo.run(f"rm {conf_path}", lambda: os.remove(conf_path))
            else:
                target_name, conf_name, variant = self.crepo.parse_path(conf)
                self.rm(target_name, conf_name, variant)

    def rm(self, target_name, conf_name, variant):
        if target_name and conf_name:
            conf_path = self.crepo.get_conf_path(target_name, conf_name, variant)
            if not os.path.exists(conf_path):
                return
            self.crepo.run(f"rm {conf_path}", lambda: os.remove(conf_path))
            if len(self.crepo.get_conf_variant_paths(target_name, conf_name)) == 0:
                self.rm_conf_from_target_config(target_name, conf_name)
        elif target_name and not conf_name and not variant:
            target_path = self.crepo.get_target_path(target_name)
            self.crepo.run(f"rm -r {target_path}", lambda: shutil.rmtree(target_path))
        elif target_name and not conf_name and variant:
            for conf_name in self.crepo.get_target_config(target_name).keys():
                self.rm(target_name, conf_name, variant)
        else:
            self.crepo.error(f"Invalid path: {conf_name}", 10)

    def rm_conf_from_target_config(self, target_name, conf_name):
        target_config = self.crepo.get_target_config(target_name)
        del target_config[conf_name]
        self.crepo.run(
            f"remove {conf_name} from target config",
            lambda: self.crepo.save_target_config(target_name, target_config),
        )
