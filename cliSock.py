import socket
import time
from PIL import Image
from encrypt import Encrypt
from sock import  Sock


class cliSock(Sock):

    def setConnect(self):
        self.__Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__Sock.settimeout(self.__timeout)
        errTimes = 0
        while True:
            try:
                self.__Sock.connect(self.__add)
                self.__heartBeats()
                # 提示 连接建立
                break
            except:
                errTimes += 1
                if errTimes == self.__errLimit:
                    # 报错 无法建立链接
                    return False

        self.__monitor()
