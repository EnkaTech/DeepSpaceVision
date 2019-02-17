from comm import *
from proc import *
import cv2
import numpy as np
from networktables import NetworkTables

if __name__ == '__main__':
    print('Robota bağlanıyor')
    cam = get_robot_camera('10.69.85.2')
    print('Robota bağlandı')
    proc_table = NetworkTables.getTable('imgproc')

    while cam.isOpened:
        capture, result, contours= detect_targets(cam)
        cv2.imshow('Kamera', capture)

        # Konturları ayıkla
        goodContours = filter(cnt_test, contours)

        if len(goodContours) >= 2:
            # Konturlar etrafına kare çek ve hata hesapla
            capture = rectangle(capture, goodContours)
            r_error, h_error = calculate_errors(goodContours)

            # Sonuçları robota bildir
            proc_table.putBoolean('Target algılandı', True)
            proc_table.putNumber('Rotate error', r_error)
            proc_table.putNumber('Horizontal error', h_error)
        else:
            proc_table.putBoolean('Target algılandı', False)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


    cv2.destroyAllWindows()
