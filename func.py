import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtCore import pyqtSignal, QObject
# from PyQt5.Qt import QUrl, QImage
from PyQt5.Qt import QPixmap, QImage # 加载图片

from PIL import Image
from PIL.ImageQt import ImageQt
import socket
import time
from cliSock import cliSock
from serSock import  serSock
from test import Ui_MainWindow


IMAGE = '1'
TEXT = '2'
PAR_ERR = 1

class Function(Ui_MainWindow, QMainWindow):
    __setSock = pyqtSignal(str)

    def __init__(self):
        '''
        self.__state 记录服务状态
        self.__IP 记录IP
        self.__port 记录Port
        self.__Sock 保存服务
        self.__path 保存图片路径
        self.__busy 标记是否正在工作
        self.__errTimes 记录传输或接受过程中的错误次数
        '''
        super(Function,self).__init__()
        self.setupUi(self)

        self.__state = None
        self.__IP = None
        self.__port = None

        self.__SockObj = None # cliSock 或 serSock 对象
        self.__sock = None # 传输用的socket

        self.__path = None
        self.__isBusy = False
        self.__errTimes = 0

        self.__image = None
        self.__text = None

        self.conButton.clicked.connect(self.__setConn)
        self.disButton.clicked.connect(self.__disConn)
        self.restButton.clicked.connect(self.__clear)
        self.cli_but.clicked.connect(self.__setClient)
        self.ser_but.clicked.connect(self.__setServe)
        self.setGraph.clicked.connect(self.__selectGraph)
        self.sendGraph.clicked.connect(self.__sendGraph)
        self.sendText.clicked.connect(self.__sendText)

    def __statsErr(self):
        # 没有选 客户端 或 服务端 的错误信息
        QMessageBox.information(self, "State has not init", "Please Choose Server or Client")

    def __AddErr(self):
        # 地址输入错误 的提示信息
        QMessageBox.information(self, "InValid Add or Port", "Please type in a correct Address and Port")

    def __conErr(self):
        # 没建立连接 的提示信息信息
        QMessageBox.information(self,"Connection Error", "No Connection")

    def __timeOutErr(self):
        # 联接超时 的提示信息
        pass

    def __clear(self):
        # 清空输入
        self.Add.setText('')
        self.Port.setText('')

    def __setConn(self):
        if self.__state == None:
            # 未选择类型
            self.__statsErr()
            return False

        self.__IP = self.Add.text()
        self.__port = int(self.Port.text())

        if self.__state == 'Serve': # 建立服务端
            try:
                self.__SockObj = serSock(self.__IP, self.__port)
                if self.__SockObj.setConnect():
                    self.__sock = self.__SockObj.sock
                    self.__monitorSer()
                    pass
                else:
                    # 无法建立联接
                    pass
            except:
                self.__AddErr()
        else: # 建立客户端
            try:
                self.__SockObj = cliSock(self.__IP, self.__port)
                if self.__SockObj.setConnect():
                    self.__sock = self.__SockObj.sock
                    self.__monitorCli()
                    pass
                else:
                    # 无法建立连接
                    pass
            except:
                self.__AddErr()

    def __disConn(self, state):
        #  断开链接
        if self.__SockObj is None: # 未建立连接
            return

        button = QMessageBox.information(self, 'Interrupt Serve', 'Are you sure to interrupt the serve?',
                                         QMessageBox.Ok | QMessageBox.No)
        if button == QMessageBox.Ok:
            self.__SockObj.disConnect()

            self.__state = state
            self.__busy = False
            # self.__Sock.shutdown(2)
            # self.__Sock.close()
            self.__SockObj = None
            self.textDisp.setText("Connection Interrupt!\n")
            self.__IP = None
            self.__port = None
            self.cli_but.setDisabled(False)
            self.ser_but.setDisabled(False)

    def __setClient(self):
        # 设置状态为 客户端
        if self.__state == None  or self.__state == 'Serve' :
            self.__state = "Client"

    def __setServe(self):
        # 设置状态为 服务端
        if self.__state == None or self.__state == 'Client' :
            self.__state = "Serve"

    def __selectGraph(self):
        # 预览与展示
        self.__path = QFileDialog.getOpenFileName(self, "Select Graph", "","Image(*.jpg)")[0]
        self.__showGraph()

    def __getText(self):
        return self.textEdit.toPlainText()

    def __showGraph(self):
        self.graphDisp.setPixmap(QPixmap.fromImage(QImage(self.__path)))

    def __sendError(self, kind):
        '''
        向另一端发送错误信息 错误类型
        input:
            kind: int类型 表示错误类型
        '''
        pass

    def __sendGraph(self):
        if self.__SockObj is None:
            return False
        self.__selectGraph()
        self.__SockObj.sendImage(self.__path)

    def __sendText(self):
        if self.__SockObj is None :
            return False
        text = self.__getText()
        self.__SockObj.sendText(text)

    def __monitorSer(self):
        while True:  # 开始监听
            if self.__isBusy == True:  # 如果有任务 等待
                # time.sleep(30)
                continue

            self.__isBusy = True  # 设置监听
            try:
                conn = self.__sock.recv(1024)
                head = conn.decode()  # 假设流程正常 conn 应该为一个 header

                if head == 'BEATS':  # 收到心跳
                    try:
                        self.__sock.send('BEATS'.encode())
                    except:
                        # 无法回复心跳
                        pass

                elif head[0] != 'H':  # 不是header
                    # header 错误
                    pass
                else:
                    kind = head.split('-')[1]

                    if kind == 'TEXT':
                        length = int(head.split('-')[2])
                        self.__sock.send(conn)  # 回发 conn 确认

                        while True:
                            try:
                                conn = self.__sock.recv(length)
                                text = conn.decode()
                                if len(text) == length:
                                    self.__sock.send(str(length).encode())
                                    self.text = text
                                    self.textDisp.setText(text)
                                    print(text, '\n')
                                    break
                                else:
                                    # 未接到正确信息
                                    pass
                            except:
                                # 未接到信息
                                pass

                    elif kind == 'IMAGE':
                        mode = head.split('-')[1]
                        size = (int(head.split('-')[2]), int(head.split('-')[3]))
                        length = int(head.split('-')[-1])
                        self.__sock.send(conn)  # 回发 conn 确认

                        while True:
                            try:
                                conn = self.__sock.recv(length)
                                image = conn.decode()  # 原始图像
                                if len(image) == length:
                                    self.__sock.send(str(length).encode())
                                    self.__image = Image.frombytes(mode, size, image)
                                    qim = ImageQt(self.__image)
                                    self.graphDisp.setPixmap(QPixmap.fromImage(qim))
                                    break
                                else:
                                    # 未收到正确信息
                                    pass
                            except:
                                pass
                    else:
                        # header 错误
                        pass
                self.__isBusy = False
                time.sleep(5)
            except:
                self.__isBusy = False
                time.sleep(5)

    def __monitorCli(self):
        while True:  # 开始监听
            if self.__isBusy == True : # 如果有任务 等待
                # time.sleep(30)
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
                                    self.__text = text
                                    self.textDisp.setText(self.__text)
                                    print(text, '\n')
                                    break
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
                                    self.__image = Image.frombytes(mode, size, image)
                                    qim = ImageQt(self.__image)
                                    self.graphDisp.setPixmap(QPixmap.fromImage(qim))
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