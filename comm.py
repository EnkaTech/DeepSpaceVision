from networktables import NetworkTables
import cv2


def nt_init(ip):
    NetworkTables.initialize(server=ip)


def get_stream_link():
    cam_table = NetworkTables.getTable('CameraPublisher')
    sub_table = cam_table.getSubTable('USB Camera 0')
    a = sub_table.getEntry('streams').get()[0]
    return (a[5:] + '&type=mjpg')


def get_cv_stream():
    return cv2.VideoCapture(get_stream_link())

def get_robot_camera(ip):
    fail = True
    while fail:
        try:
            nt_init(ip)
            cap = get_cv_stream()
            fail = False
        except TypeError:
            fail = True

    return cap

if __name__ == "__main__":
    print('Robota bağlanıyor')
    cap = get_robot_camera('10.69.85.2')
    print('Bağlantı başarılı')
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(frame, 240, 255, cv2.THRESH_BINARY)
        cv2.imshow('Video', threshold)
        if cv2.waitKey(1) & 0xFF == 27:
            exit(0)
