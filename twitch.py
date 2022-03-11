import socket
import os
from threading import Thread
import threading

clients = set()
clients_lock = threading.Lock()

def listener(client, address):
    print ("Accepted connection from: ", address)
    with clients_lock:
        clients.add(client)
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            else:

                print (repr(data))
                if b'PASS' in data:
                    msg = """:tmi.twitch.tv 001 willwillwang :Welcome, GLHF!
:tmi.twitch.tv 001 willwillwang :Welcome, GLHF!
:tmi.twitch.tv 002 willwillwang :Your host is tmi.twitch.tv
:tmi.twitch.tv 003 willwillwang :This server is rather new
:tmi.twitch.tv 004 willwillwang :-
:tmi.twitch.tv 375 willwillwang :-
:tmi.twitch.tv 372 willwillwang :You are in a maze of twisty passages, all alike.
:tmi.twitch.tv 376 willwillwang :>
"""             
                    data = msg.encode('ascii')
                if b'JOIN' in data:
                    msg = """:willwillwang!willwillwang@willwillwang.tmi.twitch.tv JOIN #willwillwang
:willwillwang.tmi.twitch.tv 353 willwillwang = #willwillwang :willwillwang
""" 
                    data = msg.encode('ascii')
                with clients_lock:
                    for c in clients:
                        c.sendall(data)
                        print(data.decode('utf-8'))
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()

host = '0.0.0.0'
port = 6667

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(3)
th = []

while True:
    print ("Server is listening for connections...")
    client, address = s.accept()
    th.append(Thread(target=listener, args = (client,address)).start())

s.close()
