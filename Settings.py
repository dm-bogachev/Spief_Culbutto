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
        [(2, 0),(1, 0),  (0, 0),  (-1, 0), (-2, 0)],
            [(1, 1),  (0, 1),  (-1, 1)],
                        [(0, 2)] )
        # Балл за каждую соответствующую лунку
        all_score = (
                [15],
            [15, 55, 15],
        [30, 55, 80, 55, 30],
            [15, 55, 15],
                [15] )
        # Вероятности для вбивания 🔨
        chances = (
                [10],
            [20, 70, 20],
        [20, 70, 100, 70, 20],
            [20, 70, 20],
                [10] )
        # Вероятность для выбивания 🔨🔨🔨
        chances_kick = (            
                [80],
            [20, 70, 120],
        [20, 70, 120, 70, 120],
            [20, 70, 120],
                [80])
        
        setting_dict = {'m':m, 'rate':rate, 'size':size, 
                        'dist':dist, 'center_shift':center_shift, 'center_pt':center_pt, 
                        'all_index':all_index, 'all_score':all_score, 'chances':chances, 'chances_kick':chances_kick }
        
        return setting_dict

    @classmethod
    def CVProcess(cls):
        setting_dict = cls.Logic() # Почти все настройки логики так же используются в CV
        
        pts_src = [(916, 287), (579, 608), (901, 943), (1235, 620)] # Точки калибровки
        
        brightness=255
        contrast=100
        
        setting_dict['pts_src'] = pts_src
        setting_dict['brightness'] = brightness
        setting_dict['contrast'] = contrast
        
        return setting_dict