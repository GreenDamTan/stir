import os
import sys

PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
if not PATH in sys.path:
    sys.path.insert(0, PATH)

from magnolia.conf import android_base

class _BH9037HP5U(android_base.Android):
    SERIAL = "BH9037HP5U"
    TMP_PICTURE="%s_TMP.png" % SERIAL
    IP = ""
    PORT = ""

    NAME = "Xperia X Compact"
    WIDTH = "1280"
    HEIGHT = "720"
    MINICAP_WIDTH = "1280"
    MINICAP_HEIGHT = "720"
    LOCATE = "V"
    ROTATE = "0"

if __name__ == "__main__":
    print(eval("_BH9037HP5U.%s" % "TMP_PICTURE"))
