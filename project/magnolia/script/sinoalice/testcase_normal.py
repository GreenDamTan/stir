import os
import sys
import time

from magnolia.utility import *
from magnolia.utility import LOG as L
from magnolia.script import testcase

class TestCase(testcase.TestCase_Base):

    def arg_parse(self, parser):
        super(TestCase, self).arg_parse(parser)
        return parser

    def reinstall(self):
        L.info(self.adb.uninstall(self.get("sinoalice.uninstall"))); time.sleep(2)
        cmd = "start -a android.intent.action.VIEW -d %s" % (self.get("sinoalice.store"))
        L.info(self.adb.am(cmd)); time.sleep(2)
        while not self.search("store"): self.sleep()
        self.tap("store\\install")
        while not self.search("store\\open"): self.sleep()
        self.tap("store\\open")
        while not self.search("entrance"): self.sleep()
        return self.tap("entrance\\start")

    def maintenance(self):
        for _ in xrange(5):
            if self.search("maintenance"):
                self.tap("maintenance\\close"); time.sleep(1)
                self.adb.stop(self.get("sinoalice.app"))
                return False
        return True
