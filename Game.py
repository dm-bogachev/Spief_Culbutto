import random
import numpy as np
from CVProcess import CVProcess
from Camera import Camera
from Logic import Logic
from Robot import *

from PyQt5 import QtCore



class Game(QtCore.QObject):
    cid = QtCore.pyqtSignal(np.ndarray) # Corrected image data
    oid = QtCore.pyqtSignal(np.ndarray) # Original image data
    hole_data = QtCore.pyqtSignal(str)
    score_data = QtCore.pyqtSignal(str)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = Camera(camera_port)
        #
        self.cv = CVProcess()
        self.l = Logic()
        self.original_image = None
        self.corrected_image = None
        self.timer = QtCore.QBasicTimer()
        self.timer.start(0, self)
        self.hole = None
    '''
    def set_correction_parameters(self, brightness, contrast): # Не используется
        self.brightness = brightness
        self.contrast = contrast
    ''' 
    def get_hole(self):
        return self.hole

    def get_random_hole(self):
        hole_list = [(5, 3), (4, 2), (4, 3), (4, 4), (3, 1), (3, 2),
                    (3, 3), (3, 4), (3, 5), (2, 2), (2, 3), (2, 4), (1, 3)]
        Hole = hole_list[random.randint(0, len(hole_list)-1)]
        Speed = 1 if random.randint(0, 6) == 0 else 0
        return (Hole, Speed)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return
        # Capture frame
        frame = self.camera.get_image()
        if frame is not None:
            # Process frame
            self.original_image, self.corrected_image = self.cv.process(frame)
            # Game logic
            self.corrected_image, hole, score = self.l.process(self.corrected_image)
            # Emit info
            self.cid.emit(self.corrected_image)
            self.oid.emit(self.original_image)
            self.hole_data.emit(str(hole))
            self.score_data.emit(str(score))
            self.hole = hole

    def __del__(self):
        self.timer.stop()
