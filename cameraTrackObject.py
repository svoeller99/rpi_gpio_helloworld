import cv2 as cv
import numpy as np
from picamera2 import Picamera2
import time

# consts
FPS_POSITION = (30,60)
FPS_FONT = cv.FONT_HERSHEY_SIMPLEX
FPS_FONT_SCALE = 1.5
FPS_FONT_COLOR = (255,0,0)
FPS_THICKNESS = 3
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360

piCam = Picamera2()
piCam.preview_configuration.main.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

# state
fps=30
hue_low = 0
hue_high = 255
sat_low = 0
sat_high = 255
val_low = 0
val_high = 255

# capture trackbar values
def set_hue_low(val):
    global hue_low
    hue_low = val
def set_hue_high(val):
    global hue_high
    hue_high = val
def set_sat_low(val):
    global sat_low
    sat_low = val
def set_sat_high(val):
    global sat_high
    sat_high = val
def set_val_low(val):
    global val_low
    val_low = val
def set_val_high(val):
    global val_high
    val_high = val

# trackbars
cv.namedWindow('trackbars')
cv.createTrackbar('Hue low', 'trackbars', 0, 255, set_hue_low)
cv.createTrackbar('Hue high', 'trackbars', 0, 255, set_hue_high)
cv.createTrackbar('Sat low', 'trackbars', 0, 255, set_sat_low)
cv.createTrackbar('Sat high', 'trackbars', 0, 255, set_sat_high)
cv.createTrackbar('Val low', 'trackbars', 0, 255, set_val_low)
cv.createTrackbar('Val high', 'trackbars', 0, 255, set_val_high)

try:

    while True:
        tStart=time.time()

        frame=piCam.capture_array()
        frameHSV=cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        lower_bound = np.array([hue_low, sat_low, val_low])
        upper_bound = np.array([hue_high, sat_high, val_high])
        mask = cv.inRange(frameHSV, lower_bound, upper_bound)
        
        mask_small = cv.resize(mask, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
        frame_small = cv.resize(frame, (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)))
        object_of_interest = cv.bitwise_and(frame_small, frame_small, mask=mask_small)
        
        cv.putText(frame, f"{fps:.1f}", FPS_POSITION, FPS_FONT, FPS_FONT_SCALE, FPS_FONT_COLOR, FPS_THICKNESS)
        cv.imshow("piCam",frame)
        cv.imshow('mask', mask_small)
        cv.imshow('Object of interest', object_of_interest)
        if cv.waitKey(1) == ord('q'):
            break
        tEnd=time.time()
        elapsed_time = tEnd - tStart
        fps=.95*fps + .05*(1/elapsed_time)
        #print(f"{fps:.1f}")

except KeyboardInterrupt:
    print('bye')

cv.destroyAllWindows()
