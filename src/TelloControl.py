import socket
import threading

class TelloControl:
    def __init__(self):
        self.local_addr = ('192.168.10.2', 9000)
        self.tello_addr = ('192.168.10.1', 8889)

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
    
    def send_command(self, command):
        self.socket.sendto(command.encode(encoding='utf-8'), self.tello_addr)

    def takeoff(self):
        self.send_command('takeoff')

    def connect(self):
        self.send_command('command')

    def streamon(self):
        self.send_command('streamon')

    def streamoff(self):
        self.send_command('streamoff')
    
    def land(self):
        self.send_command('land')
    
    def send_rc(self, rc):
        a, b, c, d = rc
        self.send_command(f'rc {a} {b} {c} {d}')

    def stop(self):
        self.socket.close()