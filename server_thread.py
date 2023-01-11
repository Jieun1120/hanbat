from socket import *
import serial
import threading

#socket
SERVER = ''
PORT = 9999
ADDR = (SERVER, PORT)

# serial
port = '/dev/ttyACM0'
boadrate = 9600

# data
SIZE = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

client_list = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)

        if msg:
            if msg == DISCONNECT_MSG:
                connected = False 
            elif msg == "SerBot":
                client_list[msg] = conn
            elif msg == "clean" or msg == "feed":
                seri.write(msg.encode(FORMAT))
            elif msg == "trace" or msg == "cancel" or msg == "call" or msg == "stop" or msg == "eat":
                sock = client_list["SerBot"]
                sock.sendall(msg.encode(FORMAT))

            print(f"[{addr}] {msg}")

    conn.close()

seri = serial.Serial(port, boadrate, timeout = None)

print(f"[ARDUINO CONNECTION] {seri.name}")

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
print("[STARTING] server is starting...")

server.listen()
print("[STARTING] server is listening...")

while True:
    conn, addr = server.accept() 
    thread = threading.Thread(target = handle_client, args = (conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

server.close()

