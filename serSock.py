import socket
from PIL import Image
import time
from encrypt import Encrypt
import threading


class serSock:

    def __init__(self, IP, port):
        self.__IP = IP
        self.__port = port
        self.__add = (self.__IP, self.__port)
        self.__encryption = Encrypt()

        self.image = None
        self.text = None

        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.bind((self.__IP, self.__port))
        self.__s.listen(2)
        self.__cli = None
        self.lock = threading.Lock()

    def setConnect(self):
        print('Waiting for connection...')
        while True:
            self.__cli, add = self.__s.accept()
            try:
                conn_bytes = self.__cli.recv(1024)
                if conn_bytes.decode() == 'BEATS':
                    self.__cli.send('BEATS'.encode())
                    print('connect to', add[0], ':', add[1])
                    return True
            except:
                print('Waiting for connection...')
                pass

    def disConnect(self):
        self.__cli.send('CLOSE'.encode())
        self.__cli.shutdown(2)
        self.__cli.close()
        self.__s.shutdown(2)
        self.__s.close()
        print("Connection interrupted!")

    def monitor(self, textShow, imgShow):
        # textShow 为文字展示函数 在这里传递 print
        th_mon = threading.Thread(target=serSock.__monitor, args=(self, textShow, imgShow))
        try: # 可能在lock时 使用者手贱点好几次，会发生重复启动报错
            th_mon.start()
            print('Monitor thread start!')
        except:
            pass

    def sendText(self, text):
        text = self.__encryption.TextEncrypt(text)
        th_sendText = threading.Thread(target=serSock.__sendText, args=(self, text))
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
        th_sendImg = threading.Thread(target=serSock.__sendImg, args=(self, img))
        try:
            th_sendImg.start()
            print('Start send Image')
        except:
            pass

    def __monitor(self, textShow, imgShow):
        while True:
            self.lock.acquire()
            try:
                self.__cli.settimeout(3) # 防止持续阻塞
                conn_bytes = self.__cli.recv(1024)
                conn = conn_bytes.decode()

                if conn[0] == 'H':
                    self.__cli.settimeout(None)  # 收到 header 恢复阻塞
                    if conn.split('-')[1] == 'TEXT':
                        self.__getText(conn, textShow)
                    elif conn.split('-')[1] == 'IMG':
                        self.__getImg(conn, imgShow)
                    else:
                        print('BAD HEADER!')
                elif conn == 'BEATS':
                    self.__cli.send('BEATS'.encode())
                    print('Get BEATS')
                elif conn == 'CLOSE':
                    self.__cli.shutdown(2)
                    self.__cli.close()
                    self.__s.shutdown(2)
                    self.__s.close()
                    print('Connect interrupted!')
                    break
                else:
                    print('Error message!')
                    break
            except:
                pass

            self.__cli.settimeout(None)
            self.lock.release()
            time.sleep(3)

    def __getText(self, head, textShow):
        '''
        input:
            textShow 传入参数为u一个tuple (head, conn)
        '''
        self.__cli.send(head.encode())
        length = int(head.split('-')[-1])

        while True:
            conn_bytes = self.__cli.recv(length)
            # conn = conn_bytes.decode()
            if len(conn_bytes) == length:
                self.__cli.send(str(length).encode())

                textShow((head, conn_bytes))

                break
            else:
                print('ERROR: get wrong text')

    def __getImg(self, head, imgShow):
        '''
        input:
            imgShow 传入参数为一个tuple (head, conn)
        '''
        self.__cli.send(head.encode())
        length = int(head.split('-')[-1])
        while True:
            conn_bytes = self.__cli.recv(length)
            if len(conn_bytes) == length:
                self.__cli.send(str(length).encode())
                imgShow((head, conn_bytes))
                break
            else:
                print('ERROR: get wrong image')

    def __sendText(self, text):
        self.lock.acquire()
        length = len(text.encode())
        head = 'H-TEXT-' + str(length)
        self.__cli.send(head.encode())
        self.__cli.settimeout(None)
        try:
            head_bytes = self.__cli.recv(1024)
            if head_bytes.decode() == head:
                self.__cli.send(text.encode())
                length_bytes = self.__cli.recv(1024)
                if length_bytes.decode() == str(length):
                    print('Client get message successfully')
                else:
                    print('ERROR : Return Wrong Length!')
            else:
                print('ERROR : Return Wrong header!')
        except:
            print('ERROR : Client does n\'t get the Header!')
        self.lock.release()

    def __sendImg(self, img):
        self.lock.acquire()
        mode = img.mode # str
        img_bytes = img.tobytes() # bytes
        length = len(img_bytes)
        width, height = img.size
        head = 'H-IMG-' + mode + '-' + str(width) + '-' + str(height) + '-' + str(length)
        self.__cli.send(head.encode())

        try:
            head_bytes = self.__cli.recv(1024)
            if head_bytes.decode() == head:
                self.__cli.send(img_bytes)
                length_bytes = self.__cli.recv(1024)
                if length_bytes.decode() == str(length):
                    print('Client get Image successfully!')
                else:
                    print('ERROR : Return Wrong Length')
            else:
                print('ERROR : Return Wrong Header!')
        except:
            print('ERROR : Client does n\'t get the Header!')
        self.lock.release()

def textShow(content):
    # content : (head, text)
    text = content[-1].decode()
    print('Client:', text)

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
    server = serSock('127.0.0.1', 21)
    server.setConnect()
    server.monitor(textShow, imgShow) # 监控
    server.sendText('try to send a text')
