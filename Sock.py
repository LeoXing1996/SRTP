import socket
import time
from PIL import Image
from encrypt import Encrypt


class Sock:
    def __init__(self, IP, port, retryTimes=3, timeout=10):
        self.__IP = IP
        self.__port = port
        self.__add = (self.__IP, self.__port)
        self.__sock = None
        self.__isBusy = False
        self.__errLimit = retryTimes
        self.__timeout = timeout
        self.__encryption = Encrypt()

        self.image = None
        self.text = None

    def setConnect(self):
        # 随子类方法变动
        # 留给子类定义
        pass

    def __monitor(self):
        while True:  # 开始监听
            if self.__isBusy == True : # 如果有任务 等待
                time.sleep(30)
                continue

            self.__isBusy = True # 设置监听
            try:
                conn = self.__sock.recv(1024)
                head = conn.decode() # 假设流程正常 conn 应该为一个 header
                if head[0] != 'H':
                    # header 错误
                    pass
                else :
                    kind = head.split('-')[1]

                    if kind == 'TEXT' :
                        length = conn.split('-')[2]
                        self.__sock.send(conn) # 回发 conn 确认

                        while True:
                            try:
                                conn = self.__sock.recv(length)
                                text = conn.decode()
                                if len(text) == length:
                                    self.__sock.send(str(length).encode())
                                    self.text = text
                                else :
                                    # 未接到正确信息
                                    pass
                            except:
                                # 未接到信息
                                pass

                    elif kind == 'IMAGE' :
                        mode = head.split('-')[1]
                        size = (int(head.split('-')[2]), int(head.split('-')[3]))
                        length = head.split('-')[-1]
                        self.__sock.send(conn) # 回发 conn 确认

                        while True :
                            try:
                                conn = self.__sock.recv(length)
                                image = conn.decode()
                                if len(image) == length :
                                    self.__sock.send(str(length))
                                    self.image = Image.frombytes(mode, size, image)
                                else:
                                    # 未收到正确信息
                                    pass
                            except:
                                pass
                    else :
                        # header 错误
                        pass
                self.__isBusy = False
                time.sleep(30)
            except:
                # 对方未发送 进行一次心跳
                self.__heartBeats()
                self.__isBusy = False
                time.sleep(30)
        pass

    def disConnect(self):
        if self.__isBusy == False:
            self.__sock.shutdown(2)
            self.__sock.close()
        else :
            # 正在工作 无法关闭
            return False

    def __heartBeats(self):
        '''
        return :
            True : 表示连接正常
            False : 表示断开
        '''
        beats = "BEATS".encode()
        res = self.__sendAndConf(beats, beats)
        return res

    def sendText(self, text):
        if self.__isBusy == True:
            return False
        self.__isBusy = True

        text = self.__encryption.TextEncrypt(text)
        length = str(len(text))
        head = 'H-TEXT-' + length

        if self.__sendHead(head.encode()) == False:
            return False
        if self.__sendTextB(text.encode(), length.encode()) == False:
            return False
        self.__isBusy = False
        return True

    def sendImage(self, path):
        '''
        input :
            path 图片路径
        return :
            True : 发送成功
            False : 发送失败
        '''
        if self.__isBusy == True: # 正在接收数据
            # 增加报错
            return False
        self.__isBusy = True
        image = self.__getImage(path)
        if image == None:
            # path error
            return False

        mode = image.mode
        image_bytes = image.tobytes()
        size = image.size
        length = len(image_bytes)
        head = 'H-IMG-' + mode + '-' + str(size[0]) + '-' + str(size[1]) + '-' + str(length)

        if self.__sendHead(head.encode()) == False:
            return False
        if self.__sendImageB(image_bytes, str(length).encode()) == False :
            return False
        self.__isBusy = False
        return True

    def __sendHead(self, head):
        # head : bytes 类型
        res = self.__sendAndConf(head, head)
        return res

    def __sendImageB(self, image_bytes,length):
        # image_bytes , length : bytes 类型
        res = self.__sendAndConf(image_bytes, length)
        return res

    def __sendTextB(self, text_bytes, length):
        # text_bytes , length : bytes 类型
        res = self.__sendAndConf(text_bytes, length)
        return res

    def __sendAndConf(self, toSend, toConf):
        '''
        input :
            toSend : bytes 类型
            toConf : bytes 类型
        return :
            True : 正确运行
            False :  错误运行
        '''
        errTimes = 0
        while True:
            try:
                self.__sock.send(toSend)
                while True :
                    try:
                        conn = self.__sock.recv(1024)
                        if conn == toConf:
                            return True
                        else:
                            errTimes += 1
                            if errTimes == self.__errLimit:
                                # 报错 回复信息不正确
                                return False
                    except:
                        errTimes += 1
                        if errTimes == self.__errLimit :
                            # 报错 无法接收
                            return False
                    time.sleep(3)
            except:
                errTimes += 1
                if errTimes == self.__errLimit:
                    # 报错 无法发送
                    return False
            time.sleep(3)

    def getImage(self, path):
        '''
        input :
            path : 图片地址
        return :
            image : PIL.Image 类型
        '''
        try:
            image = Image.open(path)
            return self.__encryption.ImageEncrypt(image)
        except:
            return None

    @property
    def IP(self):
        return self.__IP

    @property
    def port(self):
        return self.__port

    @property
    def add(self):
        return self.__add

    @property
    def isBusy(self):
        return self.__isBusy

    @property
    def errLimit(self):
        return self.__errLimit

    @property
    def timeout(self):
        return self.__timeout