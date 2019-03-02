#!/usr/bin/env python3

import cv2
import numpy as np

def detect_targets(cap):
    #Bir kare al
    ret, capture = cap.read()
    # Gürültü kaldırma için gerekli kerneller
    kernel = np.ones((9,9),np.uint8)
    kernel2 = np.ones((13,13),np.uint8)
    if ret:
        # Beyazlık filtresi
        gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray, (3, 3))
        _, filter1 = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)
        # Arkaplandaki beyaz noktaları ve cisim üzerindeki siyah noktaları yok et
        filter1 = cv2.morphologyEx(filter1, cv2.MORPH_OPEN, kernel)
        filter1 = cv2.morphologyEx(filter1, cv2.MORPH_CLOSE, kernel2)
        #Kontur bul
        contours, hierarchy = cv2.findContours(filter1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return capture, filter1, contours
    else:
        return None, None, None,

def rectangle(img, contours):
    try:
        cnt1 = contours[0]
        cnt2 = contours[1]
    except IndexError:
        return img
    #Targetları dikdörtgen içine al
    rect1 = cv2.minAreaRect(cnt1)
    box1 = cv2.boxPoints(rect1)
    rect2 = cv2.minAreaRect(cnt2)
    box1 = np.int0(box1)
    box2 = cv2.boxPoints(rect2)
    box2 = np.int0(box2)
    cv2.drawContours(img,[box1],0,(0,0,255),2)
    cv2.drawContours(img,[box2],0,(0,0,255),2)
    return img

def cnt_test(cnt):
    #0.24
    rect = cv2.minAreaRect(cnt)
    width  = min(rect[1][0], rect[1][1])
    height = max(rect[1][0], rect[1][1])
    ratio = width/height
    if cv2.contourArea(cnt) > 200 and ratio > 0.35 and ratio < 0.6:
        return True
    else:
        return False
def maap(x, in_min,  in_max,  out_min,  out_max): 
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def calculate_errors(contours):
    try:
        cnt1 = contours[0]
        cnt2 = contours[1]
    except IndexError:
        return False, 0, 0
    #Target etrafında dikdörtgensel bölge oluştur
    rect1 = cv2.minAreaRect(cnt1)
    width1  = min(rect1[1][0], rect1[1][1])
    height1 = max(rect1[1][0], rect1[1][1])
    ratio1  = width1/height1
    box1 = cv2.boxPoints(rect1)
    box1 = np.int0(box1)
    rect2 = cv2.minAreaRect(cnt2)
    box2 = cv2.boxPoints(rect2)
    width2  = min(rect2[1][0], rect2[1][1])
    height2 = max(rect2[1][0], rect2[1][1])
    ratio2  = width2/height2
    box2 = np.int0(box2)
    M1 = cv2.moments(box1)
    M2 = cv2.moments(box2)
    c1 = int(M1['m10']/M1['m00'])
    c2 = int(M2['m10']/M2['m00'])
    average = (c1+c2)/2
    z_error = average - 320
    print(ratio1)
    print(ratio2)
    #Target genişliği arasındaki fark -> Dönme hatası
    z_error = maap(z_error, -320, 320,  -30, 30)
    #Targetların ekran merkezine olan uzaklığı arasındaki fark -> Y eksenindeki hata
    y_error = (320-c1) + (320-c2)
    return True, z_error, y_error


if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    while cam.isOpened():
        capture, result, contours= detect_targets(cam)
        result = rectangle(capture, contours, hierarchy)
        if capture is None:
            print('Görüntü yok!')

        else:
            cv2.imshow('Image', capture)
            cv2.imshow('Filter', result)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
