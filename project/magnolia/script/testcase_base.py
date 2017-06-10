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
        self.service = MinicapService("minicap", self.get("args.serial"),
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
        """
        parser.add_argument('-m', action='store', dest='mobile',
                            help='Mobile (Android) Serial ID.')
        parser.add_argument('-a', action='store', dest='attack',
                            help='Attack ID.')
        parser.add_argument('-d', action='store', dest='deploy',
                            help='Deploy Fleet Number.')
        parser.add_argument('-f', action='store', dest='fleet',
                            help='Fleet Number. (1 ~ 4)')
        parser.add_argument('-e', action='store', dest='expedition',
                            help='Expedition ID.')
        parser.add_argument('-j', action='store', dest='job',
                            help='Jenkins Job.')
        parser.add_argument('-t', action='store', dest='timeout',
                            help='Timeout.')
        parser.add_argument('-u', action='store', dest='url',
                            help='target Jenkins URL.')
        parser.add_argument('-s', action='store', dest='slack',
                            help='target slack api token.')
        parser.add_argument('-c', action='store', dest='config',
                            help='Configure File.')
        parser.add_argument('-i', action='store', dest='userid',
                            help='jenkins userid.')
        parser.add_argument('-p', action='store', dest='token',
                            help='jenkins api token.')
        """
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
        """
        if cls.get("args.slack") == None:
            serial = cls.get("slack.serial")
        else:
            serial = cls.get("args.slack")
        cls.slack = cls.service["alize.slack"].get(serial)
        """

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
