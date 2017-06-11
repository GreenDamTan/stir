import os
import sys
import time
import random

from magnolia.utility import *
from magnolia.utility import LOG as L
from magnolia.script import testcase

class TestCase(testcase.TestCase_Base):

    def arg_parse(self, parser):
        super(TestCase, self).arg_parse(parser)
        return parser

    def sleep(self, base=4):
        sleep_time = (base - 0.5 * random.random())
        #L.debug("sleep time : %s" % sleep_time)
        time.sleep(sleep_time)

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

    def terms(self):
        while not self.search("entrance\\terms"): self.sleep()
        self.sleep();
        return self.tap("entrance\\terms\\yes")

    def initial_gacha(self):
        while not self.search("entrance\\initial"): self.sleep()
        while not self.search("gacha\\initial"):
            self.tap("basic\\message"); self.sleep()
        self.tap("gacha\\initial")
        return self.__gacha("initial_gacha.png")

    def __gacha(self, filename="capture.png"):
        w = int(self.adb.get().MINICAP_WIDTH)
        h = int(self.adb.get().MINICAP_WIDTH)
        while not self.search("gacha\\start"): self.sleep()
        box = POINT(w / 2, h * 0.2, 0, h * 0.6)
        L.info(self._swipe(box)); time.sleep(2)
        while not self.search("gacha\\open"): self.sleep()
        self.tap("gacha\\open"); self.sleep(2)
        while not self.search("basic\\ok"):
            self._tap(POINT(0, 0, w, 10)) #; self.sleep()
            if self.tap("basic\\ad"): self.sleep()
        self.minicap_screenshot(filename); time.sleep(2)
        return self.tap("basic\\ok")

    def name(self):
        while not self.search("name"):
            self.tap("basic\\message"); self.sleep()
        self.tap("name\\input"); self.sleep(4)
        self.adb.text(self.get("sinoalice.name")); self.sleep()
        self.tap("name\\end"); self.sleep()
        time.sleep(4)
        return self.tap("basic\\ok")

    def download(self):
        while not self.search("basic\\yes"):
            self._tap(POINT(0, 0, 10, 10))
        self.tap("basic\\yes"); self.sleep(3)
        while not self.search("entrance\\download"):
            self.tap("basic\\message"); self.sleep(4)
            self.tap("basic\\next")
        return self.tap("entrance\\download")

    def select(self):
        while not self.search("basic\\skip"): self.sleep()
        self.tap("basic\\skip"); time.sleep(4)
        while not self.search("basic\\skip"): self.sleep()
        self.tap("basic\\skip"); time.sleep(4)
        while not self.search("basic\\select"):
            self.tap("basic\\message"); self.sleep()
        time.sleep(4)
        self.tap("basic\\select"); self.sleep(5)
        return self.tap("basic\\ok")

    def message_skip(self):
        time.sleep(3)
        while self.tap("basic\\message"): self.sleep()
        return True

    def first_sweep(self):
        while not self.search("basic\\skip"): self.sleep()
        self.tap("basic\\skip"); time.sleep(4)
        while not self.search("basic\\skip"): self.sleep()
        self.tap("basic\\skip"); time.sleep(4)
        while not self.search("sweep"):
            self.tap("basic\\message"); self.sleep()
        self.tap("sweep"); time.sleep(2)
        while not self.search("sweep\\battle"):
            while self.tap("sweep\\enemy"): pass
        return self.tap("sweep\\battle")

    def box(self):
        while not self.search("box"): self.sleep()
        self.tap("box"); time.sleep(2)
        while not self.search("box\\done"):
            if self.tap("box\\all"):
                while not self.search("basic\\ok"):
                    self._tap(POINT(0, 0, 10, 10)); self.sleep()
                self.tap("basic\\ok"); time.sleep(1)
        return self.tap("basic\\menu\\home")

    def login_bonus(self):
        while not self.search("basic\\ok"): self.sleep()
        self.tap("basic\\ok")
        while not self.search("basic\\ok"): self.sleep()
        self.tap("basic\\ok")
        while not self.search("basic\\close"): self.sleep()
        return self.tap("basic\\close")

    def gacha(self):
        while not self.search("basic\\menu\\gacha"): self.sleep()
        self.tap("basic\\menu\\gacha"); self.sleep(6)
        self.tap("gacha\\release"); self.sleep(6)
        while not self.search("gacha\\ten"):
            self._tap(POINT(0, 0, 10, 10)); self.sleep()
        self.tap("gacha\\ten"); self.sleep(4)
        self.tap("basic\\ok"); self.sleep()
        self.__gacha("second_gacha.png"); self.sleep(6)
        self.tap("gacha\\ten"); self.sleep(4)
        self.tap("basic\\ok"); self.sleep()
        return self.__gacha("third_gacha.png")

    def inherit(self):
        while not self.search("basic\\menu\\menu"): self.sleep()
        self.tap("basic\\menu\\menu"); self.sleep()
        self.tap("menu\\inherit"); self.sleep()
        self.tap("menu\\inherit\\accept"); self.sleep()
        self.tap("menu\\inherit\\password"); self.sleep(4)
        self.adb.text(self.get("sinoalice.password")); self.sleep()
        self.tap("name\\end"); time.sleep(4)
        self.tap("basic\\ok"); time.sleep(2)
        self.minicap_screenshot("inherit.png"); time.sleep(2)
        return True
