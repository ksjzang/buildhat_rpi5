from picamera2 import Picamera2
import cv2
import numpy as np
import time
from buildhat import *
import marker

lm = Motor('A')
rm = Motor('B')
lm.off()
rm.off()

def drive(speedl, speedr):
    lm.pwm(speedl * (-0.01))
    rm.pwm(speedr * (0.01))

def stop():
    rm.stop()
    lm.stop()

def motor_control(key):
    if key == 'No Input':
        stop()
    if key == 'f':
        drive(17, 15)
    if key == 'r':
        drive(20, 0)
    if key == 'b':
        drive(-20, -20)
    if key == 'l':
        drive(0, 20)

def decision(x):
    if 100 < x <= 240:
        return 'f'
    elif x <= 100:
        return 'l'
    elif x > 240:
        return 'r'
    else:
        return 'b'

def make_black(image, threshold=75):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_gray = cv2.bitwise_not(gray_image)
    black_image = cv2.inRange(inverted_gray, threshold, 255)
    return black_image, gray_image

def find_contour_center_and_draw(gray, original_image):
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 123, 255, cv2.THRESH_BINARY_INV)

    mask = cv2.erode(thresh, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            cv2.polylines(original_image, [c], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.circle(original_image, (cx, cy), 5, (255, 0, 0), -1)

            print(f"Contour center: {cx}")
            return cx
    return None

def signal(image, path):
    signal_cascade = cv2.CascadeClassifier(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = signal_cascade.detectMultiScale(gray, 1.15, 5)
    return faces

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (320, 240)})
picam2.configure(config)
picam2.start()

time.sleep(0.05)

try:
    while True:
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_bgr_flipped = cv2.flip(frame_bgr, -1)
        black_image, gray = make_black(frame_bgr_flipped)

        markers = marker.marker_detect(cv2.bitwise_not(black_image))
        faces = signal(frame_bgr_flipped, './cascade.xml')

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame_bgr_flipped, (x, y), (x + w, y + h), (0, 255, 0), 3)
                stop()
                print('stop')
                time.sleep(3)
        
        elif markers == 114 or markers == 1156:
            stop()
            print(markers)
            time.sleep(3)
        
        else:
            drive_image = frame_bgr_flipped[150:239, :]
            drive_black, drive_gray = make_black(drive_image)
            cx = find_contour_center_and_draw(drive_black, drive_image)
            if cx is not None:
                key = decision(cx)
                print(f"Decision: {key}")
                motor_control(key)

        cv2.imshow('Processed Frame', frame_bgr_flipped)
        cv2.imshow('Processed black', cv2.bitwise_not(black_image))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    picam2.stop()
    cv2.destroyAllWindows()
    stop()
