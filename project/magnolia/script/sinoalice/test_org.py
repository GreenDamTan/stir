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
            self.assertTrue(self.terms())
            self.assertTrue(self.initial_gacha())
            self.assertTrue(self.name())
            self.assertTrue(self.download())
            self.assertTrue(self.select()); time.sleep(5)
            self.assertTrue(self.first_sweep()); time.sleep(5)
            self.assertTrue(self.message_skip())
            self.assertTrue(self.box()); time.sleep(2)
            self.assertTrue(self.login_bonus()); time.sleep(2)
            self.assertTrue(self.box()); time.sleep(5)
            self.assertTrue(self.gacha()); time.sleep(2)
            self.assertTrue(self.inherit())
            self.minicap_finish(); time.sleep(2)
            self.minicap_create_video()
        except Exception as e:
            L.warning(type(e).__name__ + ": " + str(e))
            #L.warning(traceback.print_exc())
            self.minicap_finish(); time.sleep(2)
            self.minicap_create_video()
            self.fail()

    @classmethod
    def tearDownClass(cls):
        L.info("*** End TestCase     : %s *** " % __file__)
