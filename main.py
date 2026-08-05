import cv2
import time
import calibration as clb

width = 640
height = 480
C_W = 66
C_H = 66
radius = 8
d_limit = 20
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
distance = 0
fps_counter = 0
fps = 0
flag = 0
min_max = []
int_sect = []
cfs = []

mask2 = clb.mask_calc(radius, C_W, C_H)
seconds_counter = int(time.time())

while True:
    success, img_src = cap.read()
    if flag != 1:
        img = img_src[:,:,2]
        _, img = cv2.threshold(img, 253, 0, cv2.THRESH_TOZERO)
        _, img = cv2.threshold(img, 254, 255, cv2.THRESH_TRUNC)
        #img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        masr = cv2.matchTemplate(img, mask2, cv2.TM_SQDIFF)
        min_val, _, min_idx, _ = cv2.minMaxLoc(masr)
        j_min = int(min_idx[0])
        i_min = int(min_idx[1])
    else:
        img = img_src[min_max[1][0]:min_max[1][1], min_max[0][0]:min_max[0][1], 2]
        _, img = cv2.threshold(img, 253, 0, cv2.THRESH_TOZERO)
        _, img = cv2.threshold(img, 254, 255, cv2.THRESH_TRUNC)
        # img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        masr = cv2.matchTemplate(img, mask2, cv2.TM_SQDIFF)
        min_val, _, min_idx, _ = cv2.minMaxLoc(masr)
        j_min = int(min_idx[0]) + min_max[0][0]
        i_min = int(min_idx[1]) + min_max[1][0]
        distance = int(clb.get_dist(int_sect[0][0], int_sect[0][1], int_sect[1][0], int_sect[1][1], (j_min+(C_W/2)), (i_min+(C_H/2))))

    #img_src = img

    if flag==1:
        cv2.line(img_src, int_sect[0], int_sect[1], (128,128,128), 1)
        if distance <= d_limit:
            x = float(j_min)
            y = float(i_min)
            z = clb.get_z(cfs[0], cfs[1], cfs[2], cfs[3], x)
            str_out = 'x=' + str(j_min) + ' y=' + str(i_min) + ' Z=' + format(z, ".1f")
            cv2.putText(img_src, str_out, (20, 50), cv2.FONT_ITALIC, 0.5,
                        (255, 0, 0), 1)
            str_out = 'dist=' + str(distance)
            cv2.putText(img_src, str_out, (20, 70), cv2.FONT_ITALIC, 0.5,
                        (255, 0, 0), 1)
        else:
            str_out = 'x= -  y= -  Z= - '
            cv2.putText(img_src, str_out, (20, 50), cv2.FONT_ITALIC, 0.5,
                        (255, 0, 0), 1)
            str_out = 'dist=' + str(distance)
            cv2.putText(img_src, str_out, (20, 70), cv2.FONT_ITALIC, 0.5,
                        (255, 0, 0), 1)
    else:
        str_out = 'x=' + str(j_min) + ' y=' + str(i_min)
        cv2.putText(img_src, str_out, (20, 50), cv2.FONT_ITALIC, 0.5,
                 (255, 0, 0), 1)

    if distance <= d_limit:
        cv2.rectangle(img_src, (j_min, i_min), (j_min+C_W, i_min+C_H), (0,255,0), 1)
        cv2.circle(img_src, (int(j_min+(C_W/2)), int(i_min+(C_H/2))), radius, (0, 255, 0), 1)
    min_val = float(min_val)/float(C_W*C_H)
    str_out = 'fps=' + str(fps_counter) + ' error=' + format(min_val, ".1f")
    cv2.putText(img_src, str_out, (20, 30), cv2.FONT_ITALIC, 0.5,
                 (255, 0, 0), 1)

    cv2.imshow('Output', img_src)
    if int(time.time()) > seconds_counter:
        seconds_counter = int(time.time())
        fps_counter = fps
        fps = 0
    fps += 1
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
         break
    if key == ord('1'):
         lines = str(j_min) + ' ' + str(i_min) + ' ' + str(1.0) + '\n'
         with open('data.txt', 'w', encoding='utf-8') as f:
             f.writelines(lines)
    if key == ord('2'):
         lines = str(j_min) + ' ' + str(i_min) + ' ' + str(91.0) + '\n'
         with open('data.txt', 'a', encoding='utf-8') as f:
             f.writelines(lines)
    if key == ord('3'):
         lines = str(j_min) + ' ' + str(i_min) + ' ' + str(181.0) + '\n'
         with open('data.txt', 'a', encoding='utf-8') as f:
             f.writelines(lines)
    if key == ord('4'):
         lines = str(j_min) + ' ' + str(i_min) + ' ' + str(271.0) + '\n'
         with open('data.txt', 'a', encoding='utf-8') as f:
             f.writelines(lines)
    if key == ord('r'):
         a, b, flag, int_sect, cfs = clb.get_params(width, height)
         min_max = clb.get_min_max(int_sect)
    if key == ord(']'):
         radius += 1
         mask2 = clb.mask_calc(radius, C_W, C_H)
    if key == ord('['):
         radius -= 1
         mask2 = clb.mask_calc(radius, C_W, C_H)
    if key == ord('p'):
         C_W += 2
         C_H += 2
         mask2 = clb.mask_calc(radius, C_W, C_H)
    if key == ord('o'):
         C_W -= 2
         C_H -= 2
         mask2 = clb.mask_calc(radius, C_W, C_H)