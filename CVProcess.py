import cv2
from cv2 import ROTATE_90_CLOCKWISE
import numpy as np


class CVProcess:

    def __init__(self, pts_src):
        self.pts_src = pts_src

    def __POS2MAT_1SHIFT_CAP(self, pos):
        m = 1                              # Масштаб изображения
        # Размер кадра после преобразования матрицей
        size = (int(m*600), int(m*900), 3)
        # Расстояние между центрами крайних лунок
        dist = int(m*180)
        center_shift = (0, -230)
        center_pt = [int(l/2 + s) for l, s in zip(size, center_shift)]
        def h_shift(x, y, h=center_pt): return (int(h[1] + x), int(h[0] + y))
        pts_dst = np.array([h_shift(dist, 0), h_shift(0, -dist),
                            h_shift(-dist, 0), h_shift(0, dist)])
        pts_src = np.array(pos)
        h, status = cv2.findHomography(pts_src, pts_dst)
        return h, size

    def __warp(self, image):
        h, size = self.__POS2MAT_1SHIFT_CAP(self.pts_src)
        image = cv2.warpPerspective(image, h, (size[1], size[0]))
        return image

    def __blur(self, image, TYPE=2, size=5):
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

    def process(self, image, brightness=255, contrast=100):
        original_image = self.__warp(image)
        temp = self.__blur(original_image)
        corrected_image = self.__correct_color(temp, brightness, contrast)
        return original_image, corrected_image
