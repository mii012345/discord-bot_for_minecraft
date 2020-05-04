import socket
from struct import *
import pdb
from pprint import pprint

class Status_Get:
    def __init__(self):
        self.ip = 'localhost'
        self.port = 25565
        self.online = False
        self.name = None
        self.ac_user = None
        self.max_user = '20'
    
    def getServerStatus(self):
        req = pack('B', 0xfe)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.ip, self.port))
                s.sendall(req)
                data = s.recv(2048)
                data = data.split(b'\xA7')
                self.name = data[0][3:-1].decode('UTF-16BE')
                ac_user_b = data[1].decode()
                ac_user0 = None
                if ac_user_b[0] == '\x00':
                    ac_user0 = "0"
                self.ac_user = ac_user0 + ac_user_b[1]
                self.online = True
        except:
            self.online = False


s = Status_Get()
s.getServerStatus()
