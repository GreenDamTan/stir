import os
import sys
import time
import argparse
try:
    import configparser
except:
    import ConfigParser as configparser

from stir.script import StirTestCase

from magnolia.server import MinicapService
from magnolia.utility import *
from magnolia.utility import LOG as L

class TestCase_Unit(StirTestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase_Unit, self).__init__(*args, **kwargs)
        self.get_config()#self.get("args.config"))
        self.get_service()
        self.service = MinicapService("minicap", self.adb.get().SERIAL,
            self.adb.get().HEIGHT, self.adb.get().WIDTH,
            self.adb.get().MINICAP_HEIGHT, self.adb.get().MINICAP_WIDTH, self.adb.get().ROTATE)
        self.service.start(); time.sleep(1)

    def __del__(self):
        if self.service != None:
            self.service.stop()

    def arg_parse(self, parser):
        super(TestCase_Unit, self).arg_parse(parser)
        parser.add_argument(action='store', dest='testcase', help='TestCase Name.')
        parser.add_argument("-s", "--serial", action='store', dest="serial", help="Android Serial.")
        return parser

    @classmethod
    def get_service(cls):
        if cls.get("args.package") != None:
            prof = os.path.join(SCRIPT_DIR, cls.get("args.package"), "profile")
        else:
            prof = PROFILE_DIR
        cls.adb = cls.service["stir.android"].get(cls.get("args.serial"), prof)
        cls.minicap = cls.service["stir.minicap"].get(cls.get("minicap.ip"), int(cls.get("minicap.port")))
        cls.pic = cls.service["stir.picture"].get()

    def get_config(cls, conf=None):
        if cls.get("args.package") != None: host = os.path.join(SCRIPT_DIR, cls.get("args.package"))
        else: host = SCRIPT_DIR

        if conf == None: conf = os.path.join(host, "config.ini")
        else: conf = os.path.join(host, "config", conf + ".ini")

        try:
            config = configparser.RawConfigParser()
            cfp = open(conf, 'r')
            config.readfp(cfp)
            for section in config.sections():
                for option in config.options(section):
                    cls.set("%s.%s" % (section, option), config.get(section, option))
        except Exception as e:
            L.warning('error: could not read config file: %s' % str(e))
