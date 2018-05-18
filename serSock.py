import socket
from PIL import Image
import time
from encrypt import Encrypt
from sock import Sock

class serSock(Sock):

    def __init__(self, IP, port, listenLim=1, retryTimes=3, timeout=10):
        super(serSock, self).__init__(IP, port, retryTimes=retryTimes,
                                      timeout=timeout)
        self.__lisLim = listenLim
        self.__ser = None
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.bind((self.__IP, self.__port))
        self.__s.listen(self.__lisLim)

    def setConnect(self):
        while True:
            print('waiting for connect ...')
            try:
                self.__Sock, add = self.__s.accept()

                self.__Sock.settimeout(self.__timeout)

                if self.__Sock.recv(1024) == "BEATS".encode():
                    print("Connect to client ", add[0], add[1])
                    self.__Sock.send("BEATS".encode())
                    self.__monitor() # 联接成功 开始监听
                else:
                    # 心跳信息有问题 客户端错误
                    pass
            except:
                # 没收到信息 继续等
                print('....')
