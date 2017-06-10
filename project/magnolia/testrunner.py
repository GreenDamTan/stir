import os
import sys
import argparse

import stir

PATH = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not PATH in sys.path:
    sys.path.insert(0, PATH)

if stir.__version__ < "0.1.0":
    sys.exit("stir version over 0.1.0. : %s " % (stir.__version__))

from stir.application import StirTestRunner
from stir.workspace import Workspace

from magnolia.utility import *
from magnolia.script.testcase_base import TestCase_Unit

class TestRunner(object):
    def __init__(self):
        self.runner = StirTestRunner()
        self.workspace = Workspace(WORK_DIR)

        self.lib = self.workspace.mkdir("lib")
        self.tmp = self.workspace.mkdir("tmp")
        self.log = self.workspace.mkdir("log")
        self.report = self.workspace.mkdir("report")

        self.tmp_video = self.workspace.mkdir(os.path.join("tmp", "video"))
        self.workspace.rmdir(os.path.join("tmp", "evidence"))
        self.tmp_evidence = self.workspace.mkdir(os.path.join("tmp","evidence"))

        TestCase_Unit.register(LIB_DIR)

    def execute(self, script, package):
        self.runner.execute(script, package, SCRIPT_DIR)

    def execute_with_report(self, script, package):
        self.runner.execute_with_report(script, package, SCRIPT_DIR, REPORT_DIR)

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        sys.exit("Usage: %s <filename>" % sys.argv[0])
    test = sys.argv[1]
    runner = TestRunner()
    result = os.path.normpath(test)
    testcase = os.path.basename(result)
    package = os.path.dirname(result); TestCase_Unit.set("args.package", package)
    runner.execute_with_report(testcase, package)
