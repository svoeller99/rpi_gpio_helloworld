import cv2 as cv
import numpy as np
import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
from libcamera import Transform
from threading import Thread, Lock
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
ADJUST_PIXELS_PER_DEGREE = 50

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

GPIO.setmode(GPIO.BCM)
adjust_lock = Lock()
pan_tilt = PanTilt()
pan_tilt.start()
pan_tilt.set_tilt(60) # point upwards a bit to start

def adjust_camera_position_async(object_of_interest_center):
    print('running async camera adjust')
    Thread(target=adjust_camera_position, args=[object_of_interest_center]).run()

def adjust_camera_position(object_of_interest_center):
    global CAMERA_FOCUS_RECTANGLE_START, CAMERA_FOCUS_RECTANGLE_END, pan_tilt, adjust_lock
    
    lock_acquired = adjust_lock.acquire(blocking=False)
    if not lock_acquired:
        return
    
    try:
        horiz_delta = SCREEN_CENTER[0] - object_of_interest_center[0]
        vert_delta = SCREEN_CENTER[1] - object_of_interest_center[1]
        vert_adjust_degrees = -(vert_delta / ADJUST_PIXELS_PER_DEGREE)
        horiz_adjust_degrees = -(horiz_delta / ADJUST_PIXELS_PER_DEGREE)
        print(f"horiz_delta={horiz_delta} vert_delta={vert_delta} horiz_adjust_degrees={horiz_adjust_degrees} vert_adjust_degrees={vert_adjust_degrees}")
        if abs(vert_adjust_degrees) >= 1:
            pan_tilt.adjust_tilt(vert_adjust_degrees)
        if abs(horiz_adjust_degrees) >= 1:
            pan_tilt.adjust_pan(horiz_adjust_degrees)
    finally:
        adjust_lock.release()
    time.sleep(.1)

try:
    face_cascade = cv.CascadeClassifier('./haar/haarcascade_frontalface_default.xml')

    while True:
        tStart=time.time()

        frame=piCam.capture_array()
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(
            frame_gray, 
            1.3, # scale factor
            5,   # min neighbors
        )

        if len(faces) > 0:
            print(faces)
            for face in faces:
                x,y,w,h = face
                cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)

        # contours, junk = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # if len(contours) > 0:
            # contours = sorted(contours, key=lambda contour: cv.contourArea(contour), reverse=True)
            # cv.drawContours(frame, contours, 0, (255, 0, 0), 2)
            # largest_contour = contours[0]
            # x,y,w,h = cv.boundingRect(largest_contour)
            # object_of_interest_start = (x, y)
            # object_of_interest_end = (x + w, y + h)
            # object_of_interest_area = w * h
            # object_of_interest_center = (x + int(w/2), y + int(h/2))
            # if object_of_interest_area >= OBJECT_OF_INTEREST_MIN_AREA:
            #     cv.rectangle(frame, object_of_interest_start, object_of_interest_end, (0, 0, 255), 3)
            #     # print(f"object of interest area: {object_of_interest_area}")
            #     adjust_camera_position_async(object_of_interest_center)
        
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
