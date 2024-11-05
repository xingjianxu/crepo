from ..crepo import CRepo
from .base import BaseCmd


class LnCmd(BaseCmd):

    def run(self, permit_exec=False):
        """
        crepo ln ipset.conf
        crepo -t ipset ln ipset.conf
        crepo ln @ipset/ipset.conf
        crepo -t ipset -v raw ln ipset.conf
        """
        for conf_name in self.args.confs:
            target_name, conf_name = self.crepo.get_target_and_conf_name(conf_name)
            self.crepo.link_conf(target_name, conf_name, self.args.variant, permit_exec)
