import cv2
import threading

class TelloVideo:
    def __init__(self):
        self.udp_video_addr = 'udp://@' + '0.0.0.0' + ':' + str(11111)

        #VideoCapture object
        self.cap = None
        self.frame_reader = None

    def get_video_capture(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.udp_video_addr)
        
        if not self.cap.isOpened():
            self.cap.open(self.udp_video_addr)
        
        return self.cap
    
    def get_frame_read(self):
        if self.frame_reader is None:
            self.frame_reader = FrameReader(self, self.udp_video_addr).start()
        
        return self.frame_reader
    
    def stop(self):
        if self.frame_reader is not None:
            self.frame_reader.stop()
        if self.cap is not None:
            self.cap.release()

class FrameReader:
    def __init__(self, tello_video, address):
        tello_video.cap = cv2.VideoCapture(address)
        self.cap = tello_video.cap

        if not self.cap.isOpened():
            self.cap.open(address)
        
        self.grabbed, self.frame = self.cap.read()
        self.stopped = False

    def start(self):
        threading.Thread(target=self.update_frame, args = ()).start()
        return self

    def update_frame(self):
        while not self.stopped:
            if not self.grabbed or not self.cap.isOpened():
                self.stop()
            else:
                (self.grabbed, self.frame) = self.cap.read()
    
    def stop(self):
        self.stopped = True
