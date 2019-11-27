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
        _, filter1 = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)
        # Arkaplandaki beyaz noktaları ve cisim üzerindeki siyah noktaları yok et
        filter2 = cv2.morphologyEx(filter1, cv2.MORPH_OPEN, kernel)
        filter3 = cv2.morphologyEx(filter2, cv2.MORPH_CLOSE, kernel2)
        #Kontur bul
        contours, _ = cv2.findContours(filter3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return capture, contours
    else:
        return None, None

def rectangle(img, contours):
    try:
        cnt1 = contours[0]
        cnt2 = contours[1]
    except IndexError:
        return img
    #Targetları dikdörtgen içine al
    rect1 = cv2.minAreaRect(cnt1)
    box_p1 = cv2.boxPoints(rect1)
    box1 = np.int0(box_p1)
    rect2 = cv2.minAreaRect(cnt2)
    box_p2 = cv2.boxPoints(rect2)
    box2 = np.int0(box_p2)
    cv2.drawContours(img,[box1],0,(0,0,255),2)
    cv2.drawContours(img,[box2],0,(0,0,255),2)
    return img

def cnt_test(cnt):
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
    box_p1 = cv2.boxPoints(rect1)
    box1 = np.int0(box_p1)

    rect2 = cv2.minAreaRect(cnt2)
    box_p2 = cv2.boxPoints(rect2)
    box2 = np.int0(box_p2)

    #Targetların ağırlık merkezini bul
    M1 = cv2.moments(box1)
    M2 = cv2.moments(box2)
    center1 = int(M1['m10']/M1['m00'])
    center2 = int(M2['m10']/M2['m00'])

    #TODO z ekseninde hata hesabı
    z_error = 0
    #Targetların ekran merkezine olan uzaklığı arasındaki fark -> Y eksenindeki hata
    y_error = (240-c1) + (240-c2)
    return True, z_error, y_error


if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    while cam.isOpened():
        capture,  contours= detect_targets(cam)
        result = rectangle(capture, contours)
        if capture is None:
            print('Görüntü yok!')

        else:
            cv2.imshow('Image', capture)
            cv2.imshow('Filter', result)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
