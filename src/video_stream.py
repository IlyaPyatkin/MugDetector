from threading import Thread

import cv2


class VideoStream:
    def __init__(self, src=0, resolution=None, threading=False, loop=False):
        self.src = src
        self.threading = threading
        self.loop = loop
        if threading:
            self.running = True
        self.stream = cv2.VideoCapture(src)
        if resolution is not None:
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.image = self.stream.read()[1]

    def __enter__(self):
        if self.threading:
            self.thread = Thread(target=self.update)
            self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.threading:
            self.running = False
            self.thread.join()
        self.stream.release()

    def update(self):
        while self.running:
            self.reset_frame()
            self.image = self.stream.read()[1]

    def read(self):
        if not self.threading:
            self.reset_frame()
            self.image = self.stream.read()[1]
        return self.image

    def reset_frame(self):
        if self.loop:
            current_frame = self.stream.get(cv2.CAP_PROP_POS_FRAMES)
            sequence_length = self.stream.get(cv2.CAP_PROP_FRAME_COUNT) - 10
            if current_frame >= sequence_length:
                self.stream.set(cv2.CAP_PROP_POS_FRAMES, 0)
