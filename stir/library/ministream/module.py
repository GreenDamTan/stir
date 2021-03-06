import os
import io
import socket
import threading

from itsdangerous import bytes_to_int
from Queue import Queue

from stir import PYTHON_VERSION
from stir.log import Log
from stir.exception import *

L = Log("Minicap.Library.STiR")
MAX_SIZE = 5

if PYTHON_VERSION == 3:
    raise LibraryError("Minicap Module Can't use for Python 3.")

class Banner(object):

    def __init__(self):
        self.version = 0
        self.length = 0
        self.pid = 0
        self.real_width = 0
        self.real_height = 0
        self.virtual_width = 0
        self.virtual_height = 0
        self.orientation = 0
        self.quirks = 0

    def __str__(self):
        return "Banner [ Version = " + str(self.version) + \
                      ", Length = " + str(self.length) + \
                      ", PID = " + str(self.pid) + \
                      ", RealWidth = " + str(self.real_width) + \
                      ", RealHeight = " + str(self.real_height) + \
                      ", VirthalWidth = " + str(self.virtual_width) + \
                      ", VirthalHeight = " + str(self.virtual_height) + \
                      ", Orientation = " + str(self.orientation) + \
                      ", Quirks = " + str(self.quirks) + " ]"


class MinicapStream(object):
    __instance = None
    __mutex = threading.Lock()

    def __init__(self, ip="127.0.0.1", port=1313):
        self.IP = ip
        self.PORT = port
        self.PID = 0
        self.banner = Banner()
        self.minicap_socket = None
        self.read_image_stream_task = None

        self.push = None
        self.picture = Queue()
        self.__flag = True

    @staticmethod
    def get_builder(ip="127.0.0.1", port=1313):
        if (MinicapStream.__instance == None):
            MinicapStream.__mutex.acquire()
            if (MinicapStream.__instance == None):
                MinicapStream.__instance = MinicapStream(ip, port)
            MinicapStream.__mutex.release()
        return MinicapStream.__instance

    def get_queue(self):
        return self.picture

    def get_d(self):
        return self.picture.qsize()

    def start(self):
        self.minicap_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.minicap_socket.connect((self.IP, self.PORT))
        self.read_image_stream_task = threading.Thread(target=self.read_image_stream).start()

    def finish(self):
        self.__flag = False

    def read_image_stream(self):
        read_banner_bytes = 0
        banner_length = 2
        read_frame_bytes = 0
        frame_body_length = 0
        data_body = ""
        counter = 0

        while self.__flag:
            #L.info("Picture Queue : %s" % (self.get_d()))
            reallen = self.minicap_socket.recv(4096)
            length = len(reallen)
            if not length: continue
            cursor = 0
            while cursor < length:
                if read_banner_bytes < banner_length:
                    if read_banner_bytes == 0:
                        self.banner.version = bytes_to_int(reallen[cursor])
                    elif read_banner_bytes == 1:
                        banner_length = bytes_to_int(reallen[cursor])
                        self.banner.length = banner_length
                    elif read_banner_bytes in [2, 3, 4, 5]:
                        self.banner.pid += (bytes_to_int(reallen[cursor]) << ((read_banner_bytes - 2) * 8)) >> 0;
                    elif read_banner_bytes in [6, 7, 8, 9]:
                        self.banner.real_width += (bytes_to_int(reallen[cursor]) << ((read_banner_bytes - 6) * 8)) >> 0;
                    elif read_banner_bytes in [10, 11, 12, 13]:
                        self.banner.real_height += (bytes_to_int(reallen[cursor]) << ((read_banner_bytes - 10) * 8)) >> 0;
                    elif read_banner_bytes in [14, 15, 16, 17]:
                        self.banner.virtual_width += (bytes_to_int(reallen[cursor]) << ((read_banner_bytes - 14) * 8)) >> 0;
                    elif read_banner_bytes in [18, 19, 20, 21]:
                        self.banner.virtual_height += (bytes_to_int(reallen[cursor]) << ((read_banner_bytes - 18) * 8)) >> 0;
                    elif read_banner_bytes == 22:
                        self.banner.orientation = bytes_to_int(reallen[cursor]) * 90
                    elif read_banner_bytes == 23:
                        self.banner.quirks = bytes_to_int(reallen[cursor])
                    cursor += 1
                    read_banner_bytes += 1
                    if read_banner_bytes == banner_length:
                        L.debug(self.banner)
                elif read_frame_bytes < 4:
                    frame_body_length = frame_body_length + ((bytes_to_int(reallen[cursor])<<(read_frame_bytes * 8)) >> 0)
                    cursor += 1
                    read_frame_bytes += 1
                else:
                    if length - cursor >= frame_body_length:
                        data_body = data_body + reallen[cursor:(cursor+frame_body_length)]
                        if bytes_to_int(data_body[0]) != 0xFF or bytes_to_int(data_body[1]) != 0xD8:
                            return
                        self.picture.put(data_body)
                        if self.get_d() > MAX_SIZE: self.picture.get()
                        cursor += frame_body_length
                        frame_body_length = 0
                        read_frame_bytes = 0
                        data_body = ""
                        counter += 1
                    else:
                        data_body = data_body + reallen[cursor:length]
                        frame_body_length -= length - cursor
                        read_frame_bytes += length - cursor
                        cursor = length
