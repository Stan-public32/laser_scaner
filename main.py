#Импорт библиотеки OpenCV - cv2
import cv2
#Импорт библиотеки для работы с числами
import numpy as np


#Побитовые операции и маски
'''
#Создание переменной photo и прогрузка в нее изображения wall.jpg из папки images проекта
photo = cv2.imread('images/wall.jpg')
#Создание своего изображения через параметры изображения photo
img = np.zeros(photo.shape[:2], dtype='uint8')
#Создаем круг, белый, закрашенный, с центром в точке 0, 0 и радиусом 50
circle = cv2.circle(img.copy(), (0,0), 100, 255, -1)
#Создаем прямоугольник, залитый, белый от точки 25,25 до точки 250, 350
square  = cv2.rectangle(img.copy(), (25,25), (250,350), 255, -1)

#Выполним операцию побитовое И для пересечения множеств
img = cv2.bitwise_and(photo, photo, mask=circle)

#Выполним операцию побитовое И для пересечения множеств
#img = cv2.bitwise_and(circle, square)
#Выполним операцию побитовое ИЛИ для пересечения множеств
#img = cv2.bitwise_or(circle, square)
#Выполним операцию побитовое НЕ для пересечения множеств
#img = cv2.bitwise_not(square)
#Выполним операцию побитовое ИЛИ-НЕ для пересечения множеств
#img = cv2.bitwise_xor(circle,square)

#Открытие окна с отображением содержимого переменной img и подписью в заколовке "Output"
cv2.imshow('Output', img)
#Удержание экрана до тех пор пока пользователь его не закроет
cv2.waitKey(0)
'''

'''
Работа с примитивами

#Создание своего изображения через матрицу
photo = np.zeros((300, 300, 3), dtype='uint8')

#Окрашиваем все пиксели через срез:
photo[:] = 128, 128, 157
#Окрашиваем прямоугольную область через срез:
photo[100:150, 200:205] = 128, 255, 128
#Выводим прямоугольник без заливки
cv2.rectangle(photo, (0, 0), (150, 150), (25, 26, 250), 2)
#Выводим прямоугольник с заливкой через rectangle
cv2.rectangle(photo, (160, 20), (200, 40), (25, 250, 250), -1)

#Выводим прямую
cv2.line(photo, (160, 20), (200, 40), (250, 25, 250), 3)
#Выводим прямую в привязке к размерам изображения
cv2.line(photo, (0, photo.shape[0] // 3), (photo.shape[1] // 3 * 2, 300), (250, 250, 25), 3)

#Выводим круг
cv2.circle(photo, (photo.shape[1] // 3 * 2, photo.shape[0] // 3 * 2), (photo.shape[1] // 6), (0, 0, 0), 3)

#Выводим текст
cv2.putText(photo, 'Solution', (photo.shape[1] // 3, photo.shape[0] // 3 * 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

#Открытие окна с отображением содержимого переменной img и подписью в заколовке "Output"
cv2.imshow('Output', photo)
#Удержание экрана до тех пор пока пользователь его не закроет
cv2.waitKey(0)
'''


'''
Работа с фото изображением

#Создание переменной img и прогрузка в нее изображения wall.jpg из папки images проекта
img = cv2.imread('images/wall.jpg')
#Вывод информации о размерах кадра
#print(img.shape)
#Изменение размера изображения
#new_img = cv2.resize(img, (640, 400))
img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))
#Добавление размытия в картинку
#img = cv2.GaussianBlur(img, (3, 3), 2)
#Конвертация картинки в оттенки серого
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#Добавление фильтра по выделению границ перехода
img = cv2.Canny(img, 100, 250)

#Создание матрицы из единиц, размерами 5х5 элементов? Формат uint8
kernel = np.ones((3, 3), np.uint8)
#Обводка границ более толстой линией шириной kernel, количество раз - iterations
img = cv2.dilate(img, kernel, iterations=1)
#Сглаживание после обводки с сужением обводок
img = cv2.erode(img, kernel, iterations=1)

#Открытие окна с отображением содержимого переменной img и подписью в заколовке "Output"
cv2.imshow('Output', img)
#Открытие окна с отображением содержимого переменной img с обрезанием по пикселям и подписью в заколовке "Output"
#cv2.imshow('Output', img[100:200,0:200])
#Удержание экрана до тех пор пока пользователь его не закроет
cv2.waitKey(0)
'''



'''
Работа с видео
'''
#Захват потока видео с вебкамеры (устройство номер 0, а если несколько, то нужное)
cap = cv2.VideoCapture(0)
width = 640
cap.set(3, width)
height = 480
cap.set(4, height)

matrix = np.full((height, width), 255, dtype=np.uint8)
C_W = 80
C_H = 80
mask2 = np.full((C_H, C_W), 0, dtype=np.uint8)
center = (C_H // 2, C_W // 2)
radius = 15

y, x = np.ogrid[:C_H, :C_W]
dist_sq = (x - center[1])**2 + (y - center[0])**2
mask2[dist_sq <= radius**2] = 0

for i in range(C_H):
    for j in range(C_W):
        if dist_sq[i, j] > radius**2:
            mask2[i, j] = 255
        else:
            mask2[i, j] = 0

masr = np.full((height-C_H, width-C_W), 0, dtype=np.int8)
hC_W = int(C_W/2)
hC_H = int(C_H/2)

while True:
     success, img_src = cap.read()
     img = img_src[:,:,2]

     _, img = cv2.threshold(img, 100, 255, cv2.THRESH_TOZERO)
     _, img = cv2.threshold(img, 150, 255, cv2.THRESH_TRUNC)
     img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
     masr = cv2.matchTemplate(img, mask2, cv2.TM_SQDIFF)
     min_val, _, min_idx, _ = cv2.minMaxLoc(masr)
     j_min = int(min_idx[0])
     i_min = int(min_idx[1])

     cv2.rectangle(img_src, (j_min, i_min), (j_min+C_W, i_min+C_H), (0,255,0), 1)
     cv2.circle(img_src, (j_min+hC_W, i_min+hC_H), radius, (0, 255, 0), 1)
     cv2.putText(img_src, format(min_val, ".3f"), (20, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                 (255, 0, 0), 1)

     #Вывод кадра на экран
     cv2.imshow('Output', img_src)
     #Условие прекращения показа видео
     key = cv2.waitKey(1) & 0xFF
     if key == ord('q'):
         break
     if key == ord('1'):
         lines = str(j_min) + ' ' + str(i_min) + ' ' + str(10.0) + '\n'
         with open('data.txt', 'w', encoding='utf-8') as f:
             f.writelines(lines)
     if key == ord('2'):
         lines = str(j_min) + ' ' + str(i_min) + ' ' + str(310.0) + '\n'
         with open('data.txt', 'a', encoding='utf-8') as f:
             f.writelines(lines)