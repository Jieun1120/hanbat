import socket
import threading

SERVER = "127.0.0.1"
PORT = 9999
ADDR = (SERVER, PORT)
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

def send(client_sock):
    while True:
        data = input("input : ")
        client_sock.sendall(data.encode(FORMAT))

        if data == "close":
            client_sock.close()
            break;

def recv(client_sock):
    while True:
        data = client_sock.recv(SIZE).decode(FORMAT)
        if data:
            print(f"[{SERVER}] {data}")

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(ADDR)

"""
user = input("user : ")
client_sock.sendall(user.encode(FORMAT))
print(f"{user}님 입장하셨습니다.")
"""

thread_send = threading.Thread(target = send, args = (client_sock, ))
thread_send.start()

thread_recv = threading.Thread(target = recv, args = (client_sock, ))
thread_recv.start()
