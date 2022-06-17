from numpy import array

class setting():
  
    @classmethod
    def Logic(cls):
        # Масштаб изображения, Начальное разрешение изображения в пикселях  
        m, rate = 1, (600, 900)            
        # Разрешение изображения с учётом масштаба
        size = (int(m*rate[0]), int(m*rate[1]), 3)
        
        # Дистанция между лунками в пикселях, Координаты центральной лунки относительно центра изображения
        dist, center_shift = int(m*180), (0, -230)
        # Координаты центральной лунки 
        center_pt = [int(l/2 + s) for l, s in zip(size, center_shift)]

        # Индексы всех лунок (в системе петухайтона)
        all_index = (
                        [(0, -2)],
            [(1, -1), (0, -1), (-1, -1)],
        [(2, 0),(1, 0),  (0, 0),  (-1, 0), (-2, 0)], # --------> 
            [(1, 1),  (0, 1),  (-1, 1)],
                        [(0, 2)] )
        # Балл за каждую соответствующую лунку
        all_score = (
                [30],
            [15, 55, 15],
        [15, 55, 80, 55, 15],  # ---------> 
            [15, 55, 15],
                [30] )
        # Вероятности для вбивания 🔨
        chances = (
                [10],
            [10, 70, 20],
        [10, 30, 100, 120, 20],  # ---------> 
            [10, 40, 20],
                [10] )
        # Вероятность для выбивания 🔨🔨🔨
        chances_kick = (            
                [60],
            [120, 70, 20],
        [120, 120, 120, 70, 20],  # ---------> 
            [120, 70, 20],
                [60])
        
        setting_dict = {'m':m, 'rate':rate, 'size':size, 
                        'dist':dist, 'center_shift':center_shift, 'center_pt':center_pt, 
                        'all_index':all_index, 'all_score':all_score, 'chances':chances, 'chances_kick':chances_kick }
        
        return setting_dict

    @classmethod
    def CVProcess(cls):
        setting_dict = cls.Logic() # Почти все настройки логики так же используются в CV
        
        pts_src = [(913, 208), (572, 536), (899, 872), (1236, 548)]#[(917, 211), (579, 538), (905, 871), (1238, 548)]#[(905, 239), (572, 573), (905, 900), (1235, 571)]# Точки калибровки
        
        brightness=200
        contrast=235
        
        setting_dict['pts_src'] = pts_src
        setting_dict['brightness'] = brightness
        setting_dict['contrast'] = contrast
        
        return setting_dict