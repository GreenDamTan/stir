import os
import sys
import time
import unittest
import argparse
import importlib
import traceback

from stir.log import LOG as L
from stir.define import *
from stir.exception import *


class StirTestCase(unittest.TestCase):
    config = {}
    service = {}

    def __init__(self, *args, **kwargs):
        global service
        super(StirTestCase, self).__init__(*args, **kwargs)
        self.register(STIR_LIB)
        self.__parse()

    @classmethod
    def register(cls, host):
        if not os.path.exists(host):
            raise LibraryError("%s is not exists." % (host))
        sys.path.append(host)
        for fdn in os.listdir(host):
            try:
                if fdn.endswith(".pyc") or fdn.endswith(".py"): pass
                elif fdn.endswith("__pycache__"): pass
                else:
                    module = importlib.import_module("%s.service" % fdn)
                    cls.service[module.NAME] = module.FACTORY
            except Exception as e:
                L.warning(traceback.print_exc())
                L.warning(type(e).__name__ + ": " + str(e))

    @classmethod
    def set(cls, name, value):
        cls.config[name] = value

    @classmethod
    def get(cls, name):
        return cls.config[name]

    def __parse(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser = self.arg_parse(parser)

        results = parser.parse_args()
        for k, v in vars(results).items():
            self.set("args.%s" % k, v)

    def arg_parse(self, parser):
        # parser.add_argument(action='store', dest="package", required=True, help="TestCase Name")
        # parser.add_argument("-p", "--package", action='store', dest="package", required=False, help="TestCase Package Name")
        return parser

    @classmethod
    def get_service(cls, settings):
        pass
