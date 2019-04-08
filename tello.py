from pynput import keyboard
import socket
import threading

class Tello:
    def __init__(self, host='192.168.10.2', port=9000):
        self.locaddr = (host,port)
        self.tello_address = ('192.168.10.1', 8889)

        self.response = None

        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.flight_speed = 100

        #Socket for sending commands
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.locaddr)

        # Thread for responses from Tello
        self.receive_thread = threading.Thread(target=self.receive_info, daemon=True)
        self.receive_thread.start()

        #Enter command mode and start video steam
        self.socket.sendto(b'command', self.tello_address)
        self.socket.sendto(b'streamon', self.tello_address)
        print('Set to command mode and stream is on...')
    def __del__(self):
        self.socket.close()

    def stop(self):
        print('landing...')
        self.socket.sendto(b'land', self.tello_address)

    def receive_info(self):
        while True: 
            try:
                data  = self.socket.recv(1518)
                print(data.decode(encoding="utf-8"))
            except Exception:
                print ('\nExit . . .\n')
                print(Exception)
                break

    def keyboard_down(self, input):
        try:
            key = input.char
        except AttributeError:
            key = input
        if key == 't':
            self.socket.sendto(b'takeoff', self.tello_address)
        elif key == 'l':
            self.socket.sendto(b'land', self.tello_address)
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
        msg = f'rc {self.a} {self.b} {self.c} {self.d}'.encode(encoding='utf-8')
        self.socket.sendto(msg, self.tello_address)

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
        msg = f'rc {self.a} {self.b} {self.c} {self.d}'.encode(encoding='utf-8')
        self.socket.sendto(msg, self.tello_address)

if __name__ == '__main__':
    drone = Tello()

    with keyboard.Listener(
            on_press=drone.keyboard_down,
            on_release=drone.keyboard_release) as listener:
        listener.join()

    drone.stop()