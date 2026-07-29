import cv2
import numpy as np
import calibration as clb

'''
Video capture and process
'''
cap = cv2.VideoCapture(0)
width = 640
cap.set(3, width)
height = 480
cap.set(4, height)
a = 0.0
b = 0.0
x = 0.0
y = 0.0
z = 0.0
flag = 0

matrix = np.full((height, width), 255, dtype=np.uint8)
C_W = 80
C_H = 80
mask2 = np.full((C_H, C_W), 0, dtype=np.uint8)
center = (C_H // 2, C_W // 2)
radius = 20

yy, xx = np.ogrid[:C_H, :C_W]
dist_sq = (xx - center[1])**2 + (yy - center[0])**2
mask2[dist_sq <= radius**2] = 0

for i in range(C_H):
    for j in range(C_W):
        if dist_sq[i, j] > radius**2:
            mask2[i, j] = 0
        else:
            mask2[i, j] = 255

masr = np.full((height-C_H, width-C_W), 0, dtype=np.int8)
hC_W = int(C_W/2)
hC_H = int(C_H/2)

while True:
    success, img_src = cap.read()
    img = img_src[:,:,2]

    _, img = cv2.threshold(img, 220, 255, cv2.THRESH_TOZERO)
    _, img = cv2.threshold(img, 230, 255, cv2.THRESH_TRUNC)
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    masr = cv2.matchTemplate(img, mask2, cv2.TM_SQDIFF)
    min_val, _, min_idx, _ = cv2.minMaxLoc(masr)
    j_min = int(min_idx[0])
    i_min = int(min_idx[1])

    #img_src = img

    if flag==1:
        x = float(j_min)
        y = float(i_min)
        z = clb.get_z(a, b, x, y)
        outstr = 'x=' + str(j_min) + ' y=' + str(i_min) + ' dist=' + format(z, ".1f")
        cv2.putText(img_src, outstr, (20, 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                 (255, 0, 0), 1)
    else:
        outstr = 'x=' + str(j_min) + ' y=' + str(i_min)
        cv2.putText(img_src, outstr, (20, 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                 (255, 0, 0), 1)

    cv2.rectangle(img_src, (j_min, i_min), (j_min+C_W, i_min+C_H), (0,255,0), 1)
    cv2.circle(img_src, (j_min+hC_W, i_min+hC_H), radius, (0, 255, 0), 1)
    min_val = float(min_val)/float(C_W*C_H)
    cv2.putText(img_src, format(min_val, ".3f"), (20, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                 (255, 0, 0), 1)

    cv2.imshow('Output', img_src)
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
    if key == ord('r'):
         a, b, flag = clb.get_params()
