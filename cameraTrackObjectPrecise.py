import cv2 as cv
import numpy as np
import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from libcamera import Transform
from threading import Thread
from pan_tilt import PanTilt

# consts
FPS_POSITION = (30,60)
FPS_FONT = cv.FONT_HERSHEY_SIMPLEX
FPS_FONT_SCALE = 1.5
FPS_FONT_COLOR = (255,0,0)
FPS_THICKNESS = 3
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 468
SCREEN_CENTER = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))
OBJECT_OF_INTEREST_MIN_AREA = 5000
OBJECT_POSITION_MAX_DELTA = 30 # allow object of interest's center to differ by no more than 30 pixels from screen center
ADJUST_DEGREES_INCREMENT = 1
ADJUST_INTERVAL_SECONDS = .25
MODE_TRACK = 0
MODE_TRAIN = 1

piCam = Picamera2()
piCam.preview_configuration.main.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.transform = Transform(hflip=0, vflip=1)
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

# state
fps=30
program_mode = MODE_TRAIN
# look for yellow bottlecap by default
hue_low = 20
hue_high = 30
sat_low = 100
sat_high = 255
val_low = 100
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
def set_program_mode(val):
    global program_mode
    program_mode = val

GPIO.setmode(GPIO.BCM)
pan_tilt = PanTilt()
pan_tilt.start()

def adjust_camera_position_async(object_of_interest_center):
    print('running async camera adjust')
    Thread(target=adjust_camera_position, args=[object_of_interest_center]).run()

def adjust_camera_position(object_of_interest_center):
    global CAMERA_FOCUS_RECTANGLE_START, CAMERA_FOCUS_RECTANGLE_END, pan_tilt
    horiz_delta = SCREEN_CENTER[0] - object_of_interest_center[0]
    vert_delta = SCREEN_CENTER[1] - object_of_interest_center[1]
    
    vert_adjust_degrees = 0
    horiz_adjust_degrees = 0
    if abs(horiz_delta) > OBJECT_POSITION_MAX_DELTA:
        if horiz_delta > 0: # left of center
            horiz_adjust_degrees = -ADJUST_DEGREES_INCREMENT
        else:               # right of center
            horiz_adjust_degrees = ADJUST_DEGREES_INCREMENT
    if abs(vert_delta) > OBJECT_POSITION_MAX_DELTA:
        if vert_delta > 0:  # above center
            vert_adjust_degrees = -ADJUST_DEGREES_INCREMENT
        else:               # below center
            vert_adjust_degrees = ADJUST_DEGREES_INCREMENT

    print(f"horiz_delta={horiz_delta} vert_delta={vert_delta} horiz_adjust_degrees={horiz_adjust_degrees} vert_adjust_degrees={vert_adjust_degrees}")
    if vert_adjust_degrees != 0:
        pan_tilt.adjust_tilt(vert_adjust_degrees)
    if horiz_adjust_degrees != 0:
        pan_tilt.adjust_pan(horiz_adjust_degrees)

# trackbars
cv.namedWindow('trackbars')
cv.createTrackbar('Hue low', 'trackbars', hue_low, 255, set_hue_low)
cv.createTrackbar('Hue high', 'trackbars', hue_high, 255, set_hue_high)
cv.createTrackbar('Sat low', 'trackbars', sat_low, 255, set_sat_low)
cv.createTrackbar('Sat high', 'trackbars', sat_high, 255, set_sat_high)
cv.createTrackbar('Val low', 'trackbars', val_low, 255, set_val_low)
cv.createTrackbar('Val high', 'trackbars', val_high, 255, set_val_high)
cv.createTrackbar('Train Mode?', 'trackbars', program_mode, 1, set_program_mode)

try:
    last_camera_adjust_time = time.time()
    last_program_mode = program_mode
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

        contours, junk = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contours = sorted(contours, key=lambda contour: cv.contourArea(contour), reverse=True)
            cv.drawContours(frame, contours, 0, (255, 0, 0), 2)
            largest_contour = contours[0]
            x,y,w,h = cv.boundingRect(largest_contour)
            object_of_interest_start = (x, y)
            object_of_interest_end = (x + w, y + h)
            object_of_interest_area = w * h
            object_of_interest_center = (x + int(w/2), y + int(h/2))
            if object_of_interest_area >= OBJECT_OF_INTEREST_MIN_AREA:
                cv.rectangle(frame, object_of_interest_start, object_of_interest_end, (0, 0, 255), 3)
                # print(f"object of interest area: {object_of_interest_area}")
                if program_mode == MODE_TRACK:
                    now = time.time()
                    if now - last_camera_adjust_time > ADJUST_INTERVAL_SECONDS: # wait X seconds between camera adjustments - TODO: constant
                        last_camera_adjust_time = now
                        adjust_camera_position_async(object_of_interest_center)
                if program_mode == MODE_TRAIN and last_program_mode == MODE_TRACK: # center camera after transition to train mode
                    pan_tilt.set_pan(90)
                    pan_tilt.set_tilt(90)
                last_program_mode = program_mode
        
        cv.putText(frame, f"{fps:.1f}", FPS_POSITION, FPS_FONT, FPS_FONT_SCALE, FPS_FONT_COLOR, FPS_THICKNESS)
        cv.imshow("piCam",frame)
        # cv.imshow('mask', mask_small)
        # cv.imshow('Object of interest', object_of_interest)
        if cv.waitKey(1) == ord('q'):
            break
        tEnd=time.time()
        elapsed_time = tEnd - tStart
        fps=.95*fps + .05*(1/elapsed_time)
        #print(f"{fps:.1f}")

except KeyboardInterrupt:
    print('bye')

cv.destroyAllWindows()
pan_tilt.stop()
GPIO.cleanup()
