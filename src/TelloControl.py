import socket
import threading
from pynput import keyboard

class TelloControl:
    def __init__(self):
        self.local_addr = ('192.168.10.2', 9000)
        self.tello_addr = ('192.168.10.1', 8889)

        #left/right, for/back, up/down, yaw
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0

        self.speed = 100

        #Socket for sending commands and receiving response
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.local_addr)
        
        #Thread for responses
        self.response_thread = threading.Thread(target=self.tello_response, daemon=True)
        self.response_thread.start()
    
    def tello_response(self):
        while True:
            try:
                response, _ = self.socket.recvfrom(1024)
                print(response.decode(encoding='utf-8'))
            except Exception as e:
                print(e)
                break

    def keyboard_down(self, input):
        try:
            key = input.char
        except AttributeError:
            key = input
        if key == 't':
            self.socket.sendto('takeoff'.encode('utf-8', self.tello_addr))
            return True
        elif key == 'l':
            self.socket.sendto('land'.encode('utf-8', self.tello_addr))
            return True
        elif key == 'w':
            self.b = self.speed
        elif key == 's':
            self.b = -(self.speed)
        elif key == 'a':
            self.a = -(self.speed)
        elif key == 'd':
            self.a = self.speed
        elif key == keyboard.Key.right:
            self.d = self.speed
        elif key == keyboard.Key.left:
            self.d = -(self.speed)
        elif key == keyboard.Key.down:
            self.c = -(self.speed)
        elif key == keyboard.Key.up:
            self.c = self.speed
        msg = f'rc {self.a} {self.b} {self.c} {self.d}'
        self.socket.sendto(msg.encode(encoding='utf-8'), self.tello_addr)
    
    def keyboard_release(self, input):
        if input == keyboard.Key.esc:
            return False
        try:
            key = input.char
        except AttributeError:
            key = input
        if key == 'w' or key == 's':
            self.b = 0
        elif key == 'a' or key == 'd':
            self.a = 0
        elif key == keyboard.Key.right or key == keyboard.Key.left:
            self.d = 0
        elif key == keyboard.Key.up or key == keyboard.Key.down:
            self.c = 0
        msg = f'rc {self.a} {self.b} {self.c} {self.d}'
        self.socket.sendto(msg.encode(encoding='utf-8'), self.tello_addr)

    def connect(self):
        self.socket.sendto('command', self.tello_addr)

    def streamon(self):
        self.socket.sendto('streamon', self.tello_addr)

    def stop(self):
        self.socket.close()