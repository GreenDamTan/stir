import os
import sys
import time

from magnolia.utility import *
from magnolia.utility import LOG as L
from magnolia.script.sinoalice import testcase_normal

class TestCase(testcase_normal.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        L.info("*** Start TestCase   : %s *** " % __file__)

    def test_1(self):
        L.info("*** Capture ***")
        try:
            self.minicap_start(); time.sleep(2)
            self.assertTrue(self.reinstall()); time.sleep(2)
            self.assertTrue(self.maintenance())
            #self.tap("entrance\\start"); time.sleep(2)
            while not self.search("entrance\\terms"): self.sleep()
            self.tap("entrance\\terms")
            while not self.search("gacha\\initial"):
                self._tap(POINT(0, 0,
                    int(self.adb.get().MINICAP_WIDTH),
                    int(self.adb.get().MINICAP_HEIGHT)))
                #self.sleep()
            self.tap("gacha\\initial")
            while not self.search("gacha\\start"): self.sleep()
            box = POINT(int(self.adb.get().MINICAP_WIDTH) / 2,
                        int(self.adb.get().MINICAP_HEIGHT) * 0.2,
                        0,
                        int(self.adb.get().MINICAP_HEIGHT) * 0.6)
            L.info(self._swipe(box))
            while not self.search("gacha\\open"):
                self._tap(POINT(0, 0,
                    int(self.adb.get().MINICAP_WIDTH),
                    int(self.adb.get().MINICAP_HEIGHT)))
                #self.sleep()
            self.tap("gacha\\open"); self.sleep(2)
            while not self.search("basic\\ok"):
                self._tap(POINT(0, 0,
                    int(self.adb.get().MINICAP_WIDTH),
                    int(self.adb.get().MINICAP_HEIGHT)))
                #self.sleep()
            self.minicap_screenshot("initial_gacha.png"); time.sleep(2)
            self.tap("basic\\ok"); self.sleep(2)
            time.sleep(20)
            self.minicap_screenshot(); time.sleep(2)
            self.minicap_finish()
        except Exception as e:
            self.minicap_finish(); time.sleep(2)
            self.minicap_create_video()
            self.fail()

    @classmethod
    def tearDownClass(cls):
        L.info("*** End TestCase     : %s *** " % __file__)
