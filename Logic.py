from math import sqrt
from copy import copy
from random import randint
from cv2 import circle, split
from Settings import setting

class Logic:

    def __init__(self, sd = setting.Logic()): # Подгрузка настроек
        self.m = sd['m']
        self.size = sd['size']
        self.dist = sd['dist']
        self.center_shift = sd['center_shift']
        self.center_pt = sd['center_pt']
        self.score = [0, 0]
        self.all_index, self.all_score    = sd['all_index'], sd['all_score']
        self.chances,   self.chances_kick = sd['chances'],   sd['chances_kick']

    def __robot_index(self, point): # Получение индекса лунки робота из индекса python
        return (-point[0]+3, -point[1]+3)
    
    def __c_hole_shift(self, x ,y): # Сдвиг относительно центральной лунки
        return (int(self.center_pt[1] + x), int(self.center_pt[0] + y))

    def __hole_coord(self, index): # Определение координаты лунки на изображении
        return self.__c_hole_shift(self.dist/2*index[0], self.dist/2*index[1])

    def __rect_slise_img(self, xy_range): # Обрезка зоны, заданной краями прямоугольника
        size = self.image.shape[0:2]
        check_range = sum([xy_range[i][0] < 0 or xy_range[i]
                          [1] > size[i] for i in [0, 1]])
        if not check_range:
            return True, self.image[xy_range[0][0]:xy_range[0][1], xy_range[1][0]:xy_range[1][1]]
        return False, None

    def __circle_slise_img(self, R, mid): # Обрезка зоны, в которой вписана искомая окружность
        mid = (mid[1], mid[0])
        xy_range = [(i-R, i+R+1) for i in mid]
        return self.__rect_slise_img(xy_range)

    def __check_circle_mean(self, R, mid, metod='rect'): # Поиск среднего значения в зоне, заданной цетром и радиусом
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

    def __get_hole_status(self, center, draw_flag = True): # Определение цвета шара в лунке
        colors = ((0, 0, 255), (0, 255, 0), (255, 0, 0))
        mean = self.__check_circle_mean(15, center)

        # Значения -1 - человек, 1 - робот, 0 - пусто
        
        if mean[0] < 180:
            if mean[1] < 180:
                if draw_flag: circle(self.image, center, 40, colors[2], 3)
                return -1
            else:
                if draw_flag: circle(self.image, center, 40, colors[0], 3)
                return 1
        if draw_flag: circle(self.image, center, 40, colors[1], 3)
        return 0

    def __get_available_holes(self): # Получение списка доступных лунок, вероятности броска в них
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

    def __get_hole(self): # Выбор лунки среди доступных с учётом вероятностного поля
        hole_list = self.__get_available_holes()
        choice = randint(0, hole_list[-1][3][1]-1)
        for hole in hole_list:
            if hole[3][0] <= choice < hole[3][1]:
                return hole[0], hole[1]

    def __get_random_hole(self): # Получение случайной лунки и силы броска
        hole_list = [(5, 3), (4, 2), (4, 3), (4, 4), (3, 1), (3, 2),
                     (3, 3), (3, 4), (3, 5), (2, 2), (2, 3), (2, 4), (1, 3)]
        hole = hole_list[randint(0, len(hole_list)-1)]
        speed = 0 if randint(0, 6) == 0 else 1
        return hole, speed

    def __get_score(self): # Определение суммарного балла за лунку
        self.score = [0, 0]
        for ptl_score, ptl_index in zip(self.all_score, self.all_index):
            for pt_score, pt_index in zip(ptl_score, ptl_index):
                match self.__get_hole_status(self.__hole_coord(pt_index), False):
                    case -1: self.score[0] += pt_score # -1 - человек
                    case 1:  self.score[1] += pt_score # 1  - робот
                        
        return self.score

    def process(self, image, random_hole=True):
        self.image = copy(image)
        self.original_image = copy(image)
        self.score = self.__get_score()
        if random_hole:
            hole = self.__get_hole()
        else:
            hole = self.__get_random_hole()
        
        return self.image, hole, self.score
    