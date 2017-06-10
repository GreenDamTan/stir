import os
import sys

from magnolia.utility import *
from magnolia.utility import LOG as L
from magnolia.script import testcase_base


class TestCase_Android(testcase_base.TestCase_Unit):

    def adb_screenshot(self, filename=None):
        if filename == None: filename = "capture.png"
        L.debug("capture file : %s" % os.path.join(TMP_DIR, filename))
        return self.adb.snapshot(filename, TMP_DIR)

    def adb_tap(self, x, y):
        return self.adb.tap(x, y)
