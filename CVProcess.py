import cv2
from cv2 import ROTATE_90_CLOCKWISE
import numpy as np
from Settings import setting



class CVProcess:

    def __init__(self, sd = setting.CVProcess()):
        
        self.m = sd['m']
        self.size = sd['size']
        self.dist = sd['dist']
        self.center_pt = sd['center_pt']
        
        self.brightness = sd['brightness']
        self.contrast = sd['contrast']
        
        self.pts_src = sd['pts_src']
        self.pts_dst = self.__pts_dst()
        self.h = self.__POS2MAT()
        
    def __pts_dst(self):
        def h_shift(x, y, h=self.center_pt): return (int(h[1] + x), int(h[0] + y))
        self.pts_dst = np.array([h_shift(self.dist, 0), h_shift(0, -self.dist),
                            h_shift(-self.dist, 0), h_shift(0, self.dist)])
        return self.pts_dst

    def __POS2MAT(self, pts_src = None, pts_dst = None): # Вычисление параметров матрицы преобразования
        if pts_src == None: pts_src = self.pts_src
        if pts_dst == None: pts_dst = self.pts_dst
        self.h, status = cv2.findHomography(np.array(pts_src), np.array(pts_dst))
        return self.h

    def __warp(self, image, h_update = False): 
        if h_update: self.__POS2MAT(self.pts_src) # Не обязательно каждый раз находить новые параметры
        image = cv2.warpPerspective(image, self.h, (self.size[1], self.size[0]))
        return image

    def __blur(self, image, TYPE=2, size=5): # Размытие (0 простое/ 1 методом Гауса/ 2 через медиану)
        match TYPE:
            case 0: image = cv2.blur(image, (size, size))
            case 1: image = cv2.GaussianBlur(image, (size, size), 0)
            case 2: image = cv2.medianBlur(image, size)
        return image

    def __correct_color(self, image, brightness, contrast):  # Настройка яркости/контраста
        contrast = contrast / 100
        brightness = brightness - 255
        image = np.uint8(np.clip((contrast * image + brightness), 0, 255))
        return image

    def process(self, image):
        original_image = self.__warp(image)
        temp = self.__blur(original_image)
        corrected_image = self.__correct_color(temp, self.brightness, self.contrast)
        return original_image, corrected_image
