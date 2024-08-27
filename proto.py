import struct
import zlib
import json
import socket
def send(bmsg):
# 创建一个socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
    s.connect(('10.255.1.101', 6667))
    s.send(bmsg.encode('utf-8'))
    s.close()

class Proto:
    def __init__(self):
        self.packetLen = 0
        self.headerLen = 16
        self.ver = 0
        self.op = 0
        self.seq = 0
        self.body = ''
        self.maxBody = 2048

    def pack(self):
        self.packetLen = len(self.body) + self.headerLen
        buf = struct.pack('>i', self.packetLen)
        buf += struct.pack('>h', self.headerLen)
        buf += struct.pack('>h', self.ver)
        buf += struct.pack('>i', self.op)
        buf += struct.pack('>i', self.seq)
        buf += self.body.encode()
        return buf

    def unpack(self, buf):
        if len(buf) < self.headerLen:
            print("包头不够")
            return
        self.packetLen = struct.unpack('>i', buf[0:4])[0]
        self.headerLen = struct.unpack('>h', buf[4:6])[0]
        self.ver = struct.unpack('>h', buf[6:8])[0]
        self.op = struct.unpack('>i', buf[8:12])[0]
        self.seq = struct.unpack('>i', buf[12:16])[0]
        if self.packetLen < 0 or self.packetLen > self.maxBody:
            print("包体长不对", "self.packetLen:", self.packetLen,
                  " self.maxBody:", self.maxBody)
            return
        if self.headerLen != self.headerLen:
            print("包头长度不对")
            return
        bodyLen = self.packetLen - self.headerLen
        self.body = buf[16:self.packetLen]
        if bodyLen <= 0:
            return
        if self.ver == 0:
            # 这里做回调
            #print("====> callback:",self.body.decode('utf-8'))
            if 'msg' in self.body.decode('utf-8'):
                msg = json.loads(self.body.decode('utf-8'))
                print(msg["data"]["uname"],msg["data"]["msg"])
                send(":" + msg["data"]["uname"] +"!" + msg["data"]["uname"] + "@" + msg["data"]["uname"] + ".tmi.twitch.tv PRIVMSG  " + "#willwillwang :"+ msg["data"]["msg"] + "\r\n")
                print('sendsuc')
        else:
            return
