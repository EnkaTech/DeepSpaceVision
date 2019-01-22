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
        # BGR'yi HSV'ye çevir
        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)
        lower_range = np.array([20,0,200])
        upper_range = np.array([40,150,255])
        mask = cv2.inRange(hsv, lower_range, upper_range)
        # Filtreyi yumuşat(blur)
        blur = cv2.blur(mask, (3, 3))
        _, result = cv2.threshold(blur,127,255,cv2.THRESH_BINARY)
        # Arkaplandaki beyaz noktaları ve cisim üzerindeki siyah noktaları yok et
        result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
        result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel2)
        #Kontur bul
        im2, contours, hierarchy = cv2.findContours(result,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return capture, result, contours, hierarchy
    else:
        return None, None, None, None

#TODO: Kontur filtreleme
