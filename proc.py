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
        # Renk filtresi
        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)
        lower_range = np.array([65,100,185])
        upper_range = np.array([75,160,255])
        mask = cv2.inRange(hsv, lower_range, upper_range)
        mask = cv2.blur(mask, (3, 3))
        _, filter1 = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
        # Beyazlık filtresi
        gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray, (3, 3))
        _, filter2 = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
        # Arkaplandaki beyaz noktaları ve cisim üzerindeki siyah noktaları yok et
        filter2 = cv2.morphologyEx(filter2, cv2.MORPH_OPEN, kernel)
        filter2 = cv2.morphologyEx(filter2, cv2.MORPH_CLOSE, kernel2)
        filter1 = cv2.morphologyEx(filter1, cv2.MORPH_OPEN, kernel)
        filter1 = cv2.morphologyEx(filter1, cv2.MORPH_CLOSE, kernel2)
        result = cv2.bitwise_or(filter1,filter2)
        #Kontur bul
        contours, hierarchy = cv2.findContours(result,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return capture, result, contours, hierarchy
    else:
        return None, None, None, None

def rectangle(img, contours, hierarchy):
    try:
        cnt1 = contours[0]
        cnt2 = contours[1]
    except IndexError:
        print('Target yok')
        return img
    rect1 = cv2.minAreaRect(cnt1)
    box1 = cv2.boxPoints(rect1)
    rect2 = cv2.minAreaRect(cnt2)
    box2 = cv2.boxPoints(rect2)
    box1 = np.int0(box1)
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    x2, y2, w2, h2 = cv2.boundingRect(cnt2)
    cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
    cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(0,255,0),2)
    cv2.drawContours(img,[box1],0,(0,0,255),2)
    box2 = np.int0(box2)
    cv2.drawContours(img,[box2],0,(0,0,255),2)
    return img

def calculate_errors(contours):
    try:
        cnt1 = contours[0]
        cnt2 = contours[1]
    except IndexError:
        return False, 0, 0
    if cv2.contourArea(cnt1) < 1200 or cv2.contourArea(cnt2) < 1200 :
        print('Target yok')
        return False, 0, 0
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    x2, y2, w2, h2 = cv2.boundingRect(cnt2)
    if x2 > x1:
        z_error = w2 - w1
    else:
        z_error = w1 - w2
    y_error = x1 - (640 - (x2+w2))
    return True, z_error, y_error


if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    while cam.isOpened():
        capture, result, contours, hierarchy = detect_targets(cam)
        result = rectangle(capture, contours, hierarchy)
        if type(capture) == type(None):
            print('Görüntü yok!')

        else:
            cv2.imshow('Image', capture)
            cv2.imshow('Filter', result)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
