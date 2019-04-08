class TelloVideo:
    def __init__(self):
        self.udp_video_addr = 'udp://@' + '0.0.0.0' + ':' + str(11111)

        #VideoCapture object
        self.cap = None
        self.frame_reader = None