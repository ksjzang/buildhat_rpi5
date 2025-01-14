import time
import cv2
import numpy as np
from picamera2 import Picamera2 

# Picamera2 초기화
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (320, 240)})
picam2.configure(config)
picam2.start()

time.sleep(0.05)  # 카메라 초기화 시간 대기

try:
    while True:
        # 프레임 캡처
        frame = picam2.capture_array()

        # 컬러 공간 변환 (RGB에서 BGR로 변환)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # 화면 Flip (상하좌우 반전)
        frame_bgr_flipped = cv2.flip(frame_bgr, -1)  # flipCode=-1은 상하좌우 반전

        # 이미지 표시
        cv2.imshow("image", frame_bgr_flipped)

        # ROI 설정 및 표시
        height, width, channel = frame_bgr_flipped.shape
        roi = frame_bgr_flipped[50:height-50, 60:width-70]
        cv2.imshow("roi", roi)

        # 이미지 상하 반전 후 표시
        flip = np.flipud(frame_bgr_flipped)
        cv2.imshow("flip", flip)

        # 종료 조건
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    picam2.stop()
    cv2.destroyAllWindows()
