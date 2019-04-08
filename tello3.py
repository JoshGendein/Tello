import threading 
import socket 
import time
from pynput import keyboard
import numpy as np
import cv2

class tello:
    def __init__(self, host='192.168.10.2', port=9000):
        self.locaddr = (host,port)
        self.tello_address = ('192.168.10.1', 8889)
        self.udp_video_addr = 'udp://@' + '0.0.0.0' + ':' + str(11111)
        self.response = None
        self.stream_on = False

        self.response_timeout = 0.5  # in seconds
        self.time_between_cmds = 0.5  # in seconds
        self.last_received_command = time.time()

        # Video Capture
        self.cap = None
        self.background_frame_read = None

        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.flight_speed = 60

        #Socket for sending commands
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.locaddr)

        # Thread for responses from Tello
        self.receive_thread = threading.Thread(target=self.receive_info, daemon=True)
        self.receive_thread.start()

    def send_command_with_return(self, command):
        print('Send command: ' + command)
        self.socket.sendto(command.encode('utf-8'), self.tello_address)

    def __del__(self):
        self.socket.close()

    def receive_info(self):
        while True:
            try:
                response, _ = self.socket.recvfrom(1024)  # buffer size is 1024 bytes
                print(response)
            except Exception as e:
                print(e)
                break

    def keyboard_down(self, input):
        print('Key down event.')
        try:
            key = input.char
        except AttributeError:
            key = input
        if key == 't':
            # self.send_command_with_return('takeoff')
            self.socket.sendto('takeoff'.encode('utf-8', self.tello_address))
        elif key == 'l':
            # self.send_command_with_return('land')
            self.socket.sendto('land'.encode('utf-8', self.tello_address))
        elif key == 'w':
            self.b = self.flight_speed
        elif key == 's':
            self.b = -(self.flight_speed)
        elif key == 'a':
            self.a = -(self.flight_speed)
        elif key == 'd':
            self.a = self.flight_speed
        elif key == keyboard.Key.right:
            self.d = self.flight_speed
        elif key == keyboard.Key.left:
            self.d = -(self.flight_speed)
        elif key == keyboard.Key.down:
            self.c = -(self.flight_speed)
        elif key == keyboard.Key.up:
            self.c = self.flight_speed
        msg = f'rc {self.a} {self.b} {self.c} {self.d}'
        self.send_command_with_return(msg)

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
        self.send_command_with_return(msg)

    def get_frame_read(self):
        if self.background_frame_read is None:
            self.background_frame_read = FrameReader(self, self.udp_video_addr).start()
        return self.background_frame_read
    
    def get_video_capture(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.udp_video_addr)

        if not self.cap.isOpened():
            self.cap.open(self.udp_video_addr)

        return self.cap

    def stop(self):
        if self.stream_on:
            self.streamoff()
        if self.background_frame_read is not None:
            self.background_frame_read.stop()
        if self.cap is not None:
            self.cap.release()
        self.send_command_with_return('land')

    def connect(self):
        self.send_command_with_return('command')
    def streamon(self):
        self.send_command_with_return('streamon')

    def streamoff(self):
        self.send_command_with_return('streamoff')

class FrameReader:
    def __init__(self, tello, address):
        tello.cap = cv2.VideoCapture(address)
        self.cap = tello.cap

        if not self.cap.isOpened():
            self.cap.open(address)

        self.grabbed, self.frame = self.cap.read()
        self.stopped = False

    def start(self):
        threading.Thread(target=self.update_frame, args=()).start()
        return self

    def update_frame(self):
        while not self.stopped:
            if not self.grabbed or not self.cap.isOpened():
                self.stop()
            else:
                (self.grabbed, self.frame) = self.cap.read()

    def stop(self):
        self.stopped = True

if __name__ == '__main__':
    drone = tello()
    drone.connect()
    drone.streamon()

    with keyboard.Listener(
            on_press=drone.keyboard_down,
            on_release=drone.keyboard_release) as listener:
        listener.join()

    drone.stop()