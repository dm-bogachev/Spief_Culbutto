
import cv2

class Camera:
    
    def __init__(self, camera_port = 0):
        self.camera = self.__camera_init(camera_port)

    def __camera_init(self, path):
        camera = cv2.VideoCapture(path, cv2.CAP_ANY)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        print('Warming up the camera')
        for i in range(10):
            print('/|\\-'[i % 4]+'\r', end='')
            _, frame = camera.read()
            cv2.waitKey(100)
        return camera

    def get_image(self):
        ret, frame = self.camera.read()
        if ret:
            return frame
        return None