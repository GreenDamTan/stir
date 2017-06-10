import os
import sys

from stir.exception import *

from magnolia.utility import *
from magnolia.utility import LOG as L
from magnolia.script import testcase_base


class TestCase_Slack(testcase_base.TestCase_Unit):

    def slack_message(self, message, channel=None):
        if channel == None: channel = self.get("slack.channel")
        try:
            self.slack.message(message, channel)
        except SlackError as e:
            L.warning(str(e))

    def slack_upload(self, filepath, channel=None):
        if channel == None: channel = self.get("slack.channel")
        try:
            L.warning(os.path.exists(filepath))
            self.slack.upload(filepath, channel, filetype="image/png")
        except SlackError as e:
            L.warning(str(e))
            raise e
