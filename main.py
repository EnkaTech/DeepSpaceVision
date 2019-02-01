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
        capture = rectangle(capture, contours)

        cv2.imshow('Kamera', capture)
        success, r_error, h_error = calculate_errors(contours)
        proc_table.putBoolean('Target algılandı', success)
        proc_table.putNumber('Rotate error', r_error)
        proc_table.putNumber('Horizontal error', h_error)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


    cv2.destroyAllWindows()
