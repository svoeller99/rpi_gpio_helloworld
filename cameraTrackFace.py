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

def calculate_area(rec):
    x,y,w,h = rect
    return w * h

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
            faces_by_area = sorted(faces, key=lambda face: calculate_area(face), reverse=True)
            largest_face = faces_by_area[0]
            x,y,w,h = largest_face
            if calculate_area(largest_face) >= OBJECT_OF_INTEREST_MIN_AREA:
                cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
                face_center = (x + int(w/2), y + int(h/2))
                adjust_camera_position_async(face_center)
        
        cv.putText(frame, f"{fps:.1f}", FPS_POSITION, FPS_FONT, FPS_FONT_SCALE, FPS_FONT_COLOR, FPS_THICKNESS)
        cv.imshow("piCam",frame)
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
