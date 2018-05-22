import socket
import time
from PIL import Image
from encrypt import Encrypt
import threading


class cliSock:

    def __init__(self, IP, port):
        self.__IP = IP
        self.__port = port
        self.__add = (self.__IP, self.__port)
        self.__sock = None
        self.__isBusy = False
        self.__encryption = Encrypt()
        self.lock = threading.Lock()
        self.image = None
        self.text = None

    def setConnect(self):
        print('Waiting for connection...')
        while True:
            try:
                self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__sock.connect(self.__add)
                self.__sock.send('BEATS'.encode())

                conn_bytes = self.__sock.recv(1024)
                conn = conn_bytes.decode()

                if conn == 'BEATS':
                    print('Connect to ',self.__IP, ':', self.__port)
                    return True
                else:
                    # 没有正确收到心跳回应
                    return False
            except:
                print('Waiting for connection...')
                pass

    def disConnect(self):
        self.__sock.send('CLOSE'.encode())
        self.__sock.shutdown(2)
        print("Connection interrupted!")

    def monitor(self, textShow, imgShow):
        th_mon = threading.Thread(target=cliSock.__monitor, args=(self, textShow, imgShow))
        try:
            th_mon.start()
            print('Start monitor')
        except:
            pass

    def sendText(self, text):
        text = self.__encryption.TextEncrypt(text)
        th_sendText= threading.Thread(target=cliSock.__sendText, args=(self, text))
        try:
            th_sendText.start()
            print('Start send text')
        except:
            pass

    def sendImg(self, img):
        '''
        input:
            img: 为PIL.Image 类型 不是的话需要提前转化！！！
        '''
        img = self.__encryption.ImageEncrypt(img)
        th_sendImg = threading.Thread(target=cliSock.__sendImg, args=(self, img))
        try:
            th_sendImg.start()
            print('Start send Image')
        except:
            pass

    def __monitor(self, textShow, imgShow):
        # beats = 0  心跳计数
        while True:
            self.lock.acquire()
            try:
                self.__sock.settimeout(3)
                conn_bytes = self.__sock.recv(1024)
                conn = conn_bytes.decode()
                if conn[0] == 'H':
                    self.__sock.settimeout(None)
                    if conn.split('-')[1] == 'TEXT':
                        self.__getText(conn, textShow)
                    elif conn.split('-')[1] == 'IMG':
                        self.__getImg(conn, imgShow)
                    else:
                        print('BAD HEADER')
                elif conn == 'CLOSE':
                    self.__sock.shutdown(2)
                    self.__sock.close()
                    print('Connect interrupted!')
                    break
                else:
                    print('Error message!')
                    break
            except:
                # self.__sock.settimeout(None)  # ???
                # beats += 1
                # if beats == 3:  # 进行心跳
                #     self.__sock.send('BEATS'.encode())
                #     try:
                #        conn_bytes = self.__sock.recv(1024)
                #        conn = conn_bytes.decode()
                #        if conn == 'BEATS':
                #            print('BEATS Success!')
                #     except:
                #         print('Heart Beats Error! \n Loss Connection!')
                #         break
                #     beats = 0
                pass
            self.__sock.settimeout(None)
            self.lock.release()
            time.sleep(3)

    def __getText(self, head, textShow):
        '''
        input:
            textShow 传入参数为u一个tuple (head, conn)
        '''
        self.__sock.send(head.encode())
        length = int(head.split('-')[-1])

        while True:
            conn_bytes = self.__sock.recv(length)
            if len(conn_bytes) == length:
                self.__sock.send(str(length).encode())
                textShow((head, conn_bytes))
                break
            else:
                print('ERROR: get wrong text')

    def __getImg(self, head, imgShow):
        '''
        input:
            imgShow 传入参数为一个tuple (head, conn)
        '''
        self.__sock.send(head.encode())
        length = int(head.split('-')[-1])
        while True:
            conn_bytes = self.__sock.recv(length)
            # conn = conn_bytes.decode()
            if len(conn_bytes) == length:
                self.__sock.send(str(length).encode())
                imgShow((head,conn_bytes))
                break
            else:
                print('ERROR: get wrong image')

    def __sendText(self, text):
        self.lock.acquire()
        length = len(text.encode())
        head = 'H-TEXT-' + str(length)
        self.__sock.send(head.encode())

        try:
            head_bytes = self.__sock.recv(1024)
            if head_bytes.decode() == head:
                self.__sock.send(text.encode())
                length_bytes = self.__sock.recv(1024)
                if length_bytes.decode() == str(length):
                    print('Server get message successfully')
                else:
                    print('ERROR : Return Wrong Length!')
            else:
                print('ERROR : Return Wrong header!')
        except:
            print('ERROR : Server does n\'t get the Header!')
        self.lock.release()

    def __sendImg(self, img):
        self.lock.acquire()
        mode = img.mode # str
        img_bytes = img.tobytes() # bytes
        length = len(img_bytes)
        width, height = img.size
        head = 'H-IMG-' + mode + '-' + str(width) + '-' + str(height) + '-' + str(length)
        self.__sock.send(head.encode())

        try:
            head_bytes = self.__sock.recv(1024)
            if head_bytes.decode() == head:
                self.__sock.send(img_bytes)
                length_bytes = self.__sock.recv(1024)
                if length_bytes.decode() == str(length):
                    print('Server get Image successfully!')
                else:
                    print('ERROR : Return Wrong Length')
            else:
                print('ERROR : Return Wrong Header!')
        except:
            print('ERROR : Server does n\'t get the Header!')
        self.lock.release()


def textShow(content):
    '''
    input:
        content: 传入元组 (head, text_bytes), head 不需要在意, 主要用于与imgShow统一格式
    '''
    text = content[-1].decode()
    print('Server: ', text)

def imgShow(content):
    '''
    input:
        content: 传入元组 (head, img_bytes),
                head 为 H-IMG-MODE-WIDTH-HEIGHT-LENGTH
    '''
    img = content[-1]
    head = content[0].split('-')
    mode = head[2]
    size = (int(head[3]), int(head[4]))
    image = Image.frombytes(mode, size, img)
    image.show()

if __name__ == '__main__':
    cli = cliSock('127.0.0.1',21)
    cli.setConnect()
    cli.monitor(textShow, imgShow)
