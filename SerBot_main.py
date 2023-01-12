# import
from socket import *
import threading
from pop import LiDAR, Pilot, AudioPlay
import time

# tcp variables
SERVER = "192.168.0.19"  # Raspberry Pi
PORT = 9999
ADDR = (SERVER, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

# serbot settings
cam = Pilot.Camera(width = 300, height = 300)
lidar = LiDAR.Rplidar()
bot = Pilot.SerBot()

lidar.connect()

direction = 0
recv_data = ""

# main code
def recv(client_sock):
    while True:
        global recv_data
        recv_data = client_sock.recv(SIZE).decode(FORMAT)
        if recv_data:
            print(f"[{SERVER}] {recv_data}")
                
client_sock = socket(AF_INET, SOCK_STREAM)
client_sock.connect(ADDR)

user = "SerBot"
client_sock.sendall(user.encode(FORMAT))
print(f"{user}님 입장하셨습니다.")

thread_recv = threading.Thread(target = recv, args = (client_sock, ))
thread_recv.start()

while True:
    # trace start == Lidar, bot start
    if recv_data == "trace":
        # bot
        bot.setSpeed(33)
        #LiDAR
        lidar.startMotor()
        # OF
        OF = Pilot.Object_Follow(cam)
        OF.load_model()

        cam.show()

        while True:
            collision = True
            c = OF.detect(index = 'person')

            while collision:
                collision = False
                vectors = lidar.getVectors()

                for v in vectors:
                    degree = v[0]
                    distance = v[1]

                    left_hand = (direction - 60) % 360
                    right_hand = (direction + 60) % 360

                    disc = None

                    if left_hand > right_hand:
                        disc = degree >= left_hand or degree <= right_hand
                    else:
                        disc = degree <= left_hand and degree <= right_hand

                    if disc:
                        if distance <= 500:
                            collision = True
                            bot.stop()
                            break

                if collision:
                    direction += 30
                    direction %= 360

            bot.move(direction, 33)

            if c is not None:
                while True:
                    c = OF.detect(index = 'person')

                    if c is not None:
                        steer = c['x'] * 4

                        if steer > 1:
                            steer = 1
                        elif steer < -1:
                            steer = -1

                        bot.steering = steer

                        if c['size_rate'] < 0.20:
                            bot.forward(33)
                        else:
                            bot.stop()
                    else:
                        steer = 0
                        break

            # trace stop == LiDAR, bot stop
            if recv_data == "cancel":
                bot.stop()
                lidar.stopMotor()
                break
                
        recv_data = ""

    # voice
    elif recv_data == "call":
        try:
            with AudioPlay("나비야.wav", False, True) as play:
                play.run()

                for _ in range(1):
                    time.sleep(1)

                play.stop()
        except OSError as e:
            print("error")
            
        recv_data = ""
        
    elif recv_data == "stop":
        try:
            with AudioPlay("안돼.wav", False, True) as play:
                play.run()

                for _ in range(1):
                    time.sleep(1)

                play.stop()
        except OSError as e:
            print("error")
        
        recv_data = ""
        
    elif recv_data == "eat":
        try:
            with AudioPlay("밥먹자.wav", False, True) as play:
                play.run()

                for _ in range(1):
                    time.sleep(1)

                play.stop()
        except OSError as e:
            print("error")
            
        recv_data = ""
