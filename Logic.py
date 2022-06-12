

from math import sqrt
from copy import copy
import random

from cv2 import circle, split

class Logic:

    def __init__(self):
        self.m = 1
        self.size = (int(self.m*600), int(self.m*900), 3)
        self.dist = int(self.m*180)
        self.center_shift = (0, -230)
        self.center_pt = [int(l/2 + s)
                          for l, s in zip(self.size, self.center_shift)]
        self.h_shift = lambda x, y, h = self.center_pt: (
            int(h[1] + x), int(h[0] + y))
        self.score = None
        self.all_index = ([(0, -2)], [(1, -1), (0, -1), (-1, -1)], [(2, 0),
                          (1, 0), (0, 0), (-1, 0), (-2, 0)], [(1, 1), (0, 1), (-1, 1)], [(0, 2)])

        #self.chances = ([1], [1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1], [1])
        #self.chances_kick = ([1], [1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1], [1])

        self.chances = (
        [10],
        [20,70,20],
        [20,80,100,60,20],
        [20,70,20],
        [10]
        )

        self.chances_kick = (
        [70],
        [20,70,120],
        [20,80,120,90,120],
        [20,70,120],
        [70]
        )

        self.hole_p = [           # Параметры лунок по группам: баллы, координаты
            [15, [self.h_shift(self.dist, 0), self.h_shift(-self.dist, 0), self.h_shift(self.dist/2, self.dist/2),
                  self.h_shift(-self.dist/2, self.dist/2), self.h_shift(self.dist/2, -self.dist/2), self.h_shift(-self.dist/2, -self.dist/2)]],
            [30, [self.h_shift(0, self.dist), self.h_shift(
                0, -self.dist)]],
            [55, [self.h_shift(0, self.dist/2), self.h_shift(self.dist/2, 0),
                  self.h_shift(0, -self.dist/2), self.h_shift(-self.dist/2, 0)]],
            [80, [self.h_shift(0, 0)]]]

    def __robot_index(self, point): return (-point[0]+3, -point[1]+3)

    def __hole_coord(self, index):
        return self.h_shift(self.dist/2*index[0], self.dist/2*index[1])

    # Обрезка зоны, заданной краями прямоугольника
    def __rect_slise_img(self, xy_range):
        # xy_range = ( (xmin, xmax), (ymin, ymax) )
        size = self.image.shape[0:2]
        check_range = sum([xy_range[i][0] < 0 or xy_range[i]
                          [1] > size[i] for i in [0, 1]])
        if not check_range:
            return True, self.image[xy_range[0][0]:xy_range[0][1], xy_range[1][0]:xy_range[1][1]]
        return False, None

    # Обрезка зоны, в которой вписана искомая окружность
    def __circle_slise_img(self, R, mid):
        mid = (mid[1], mid[0])
        xy_range = [(i-R, i+R+1) for i in mid]
        return self.__rect_slise_img(xy_range)

    # Поиск среднего значения в зоне, заданной цетром и радиусом
    def __check_circle_mean(self, R, mid, metod='rect'):
        ret, SLICE = self.__circle_slise_img(R, mid)
        if ret:
            match metod:
                case 'circle':
                    glob_sum, n = [0, 0, 0], 0
                    for i in range(-R, R):
                        for j in range(1, int(sqrt(R**2 - i**2))):
                            glob_sum += SLICE[i+R, j+R] + SLICE[i+R, -j-1+R]
                            n += 2
                    return [i/n for i in glob_sum]
                case 'rect': return [int(color.sum()/len(color)/len(color[0])) for color in split(SLICE)]
        return []

    def __get_hole_status(self, center):
        colors = ((0, 0, 255), (0, 255, 0), (255, 0, 0))
        mean = self.__check_circle_mean(15, center)

        if mean[0] < 180:
            if mean[1] < 180:
                circle(self.image, center, 40, colors[2], 3)
                return -1
            else:
                circle(self.image, center, 40, colors[0], 3)
                return 1
        circle(self.image, center, 40, colors[1], 3)
        return 0

    def __get_available_holes(self):
        holes = []
        sum_prop = 0
        for i, line in enumerate(self.all_index):
            for j, index in enumerate(line):
                match self.__get_hole_status(self.__hole_coord(index)):
                    case -1:
                        prob = self.chances_kick[i][j]
                        holes.append((self.__robot_index(
                            index), 1, prob, (sum_prop, sum_prop + prob)))
                        sum_prop += prob
                        break
                    case 1: break
                    case 0:
                        prob = self.chances[i][j]
                        holes.append((self.__robot_index(
                            index), 0, prob, (sum_prop, sum_prop + prob)))
                        sum_prop += prob
        if len(holes) == 0:
            h,s = self.__get_random_hole()
            return [(h, s, 1, (0, 1))]
        return holes

    def __get_hole(self):
        hole_list = self.__get_available_holes()
        max_rand = hole_list[-1][3][1]
        choice = random.randint(0, max_rand-1)
        for hole in hole_list:
            if hole[3][0] <= choice < hole[3][1]:
                return hole[0], hole[1]

    def __get_random_hole(self):
        hole_list = [(5, 3), (4, 2), (4, 3), (4, 4), (3, 1), (3, 2),
                     (3, 3), (3, 4), (3, 5), (2, 2), (2, 3), (2, 4), (1, 3)]
        hole = hole_list[random.randint(0, len(hole_list)-1)]
        speed = 1 if random.randint(0, 6) == 0 else 0
        return hole, speed

    def __get_score(self):
        score = [0, 0]
        for ball, coords in self.hole_p:
            for center in coords:
                mean = self.__check_circle_mean(10, center)
                if mean[0] < 180:
                    if mean[1] < 180:
                        score[0] += ball
                    else:
                        score[1] += ball
        return score

    # def __set_image(self, image):
    #     self.image = copy(image)
    #     self.original_image = copy(image)

    # def __get_image(self):
    #     self.__get_available_holes()
    #     return self.image

    def process(self, image, random_hole=True):
        self.image = copy(image)
        self.original_image = copy(image)
        if random_hole:
            hole = self.__get_hole()
        else:
            hole = self.__get_random_hole()
        score = self.__get_score()
        return self.image, hole, score