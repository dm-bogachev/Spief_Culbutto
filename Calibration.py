import cv2, cv2.aruco as aruco

class calibration():
  
  def __init__(self, cap, n_points):
    self.cap = cap
    self.n_points = n_points
    self.points = tuple(range(n_points))

  @staticmethod
  def marker_center(corners,  TypeIn = int, Type = tuple):   # Вычисление центра маркера
    X_Cent = TypeIn((corners[0][0] + corners[1][0] + corners[2][0] + corners[3][0]) / 4)
    Y_Cent = TypeIn((corners[0][1] + corners[1][1] + corners[2][1] + corners[3][1]) / 4)
    return Type((X_Cent, Y_Cent))

  def MANUAL_POS(self, img):
    pts = []
    
    def mouse_callback(event,x,y,flags,param, pts = pts):
      if event == cv2.EVENT_LBUTTONDBLCLK:
        n = len(pts)
        if n == self.n_points:
          print('Список точек полон, список будет перезаписан') 
          pts.clear()

        pts.append((x,y))
        print(f'Vетка №{len(pts)} задана: {(x,y)}')
        
        if n == self.n_points-1: print(f'Список меток заполнен, полученный список {pts}')
        
      if event == cv2.EVENT_RBUTTONDBLCLK:
        print(f'Точки {pts} удалены, список будет перезаписан')
        pts.clear()
      pass

    cv2.namedWindow("Source Image", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Source Image", mouse_callback)
    while True:
      cv2.imshow("Source Image", img)
      cv2.waitKey(0)
      if len(pts) == self.n_points: 
        print('Ручная настройка точек закончена')
        cv2.destroyWindow("Source Image")
        return pts
      else: print('Ручная настройка точек не закончена, завершите настройку!')

  def AUTO_POS(self):
    
    aruco_dict, parameters = aruco.Dictionary_get(aruco.DICT_4X4_50), aruco.DetectorParameters_create()
    def aruco_scan(frame):  # Распознавание меток
      corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
      aruco.drawDetectedMarkers(frame, corners, ids,borderColor=(0, 255, 0))
      aruco.drawDetectedMarkers(frame, rejectedImgPoints, borderColor=(100, 0, 240))
      
      center_dict = {}  # координаты цетров меток
      if not(ids is None):
          for i in range(len(corners)):
              marker_pts = [point for point in corners[i][0]]
              center_dict[ids[i][0]] = self.marker_center(marker_pts)
      return center_dict
    while True:
      _, img = self.cap.read()
      center_dict = aruco_scan(img)
      
      pos = [center_dict.get(i) for i in self.points]
      if not(None in pos):
        print(f'Все метки считаны: {pos}')
        return pos

      cv2.imshow("Source Image", img)
      if cv2.waitKey(1) == 27:
        print('Считывание прервано')
        return None
  

if __name__ == '__main__':
  cap = cv2.VideoCapture(1, cv2.CAP_ANY)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1920)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
  _, im_src = cap.read()

  calibrator = calibration(cap, 4)
  pts_src = calibrator.AUTO_POS()
  #pts_src = MANUAL_POS(im_src)
  print(pts_src)