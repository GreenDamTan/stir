__version__ = (0, 1, 0)
import os
import sys

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from ministream import module
from ministream.module import MinicapStream

class Factory(object):
    def __init__(self):
        pass

    def version(self):
        return __version__

    def get(self, ip, port):
        return MinicapStream.get_builder(ip, port)


NAME = "stir.minicap"
FACTORY = Factory()
