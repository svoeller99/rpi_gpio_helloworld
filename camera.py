import cv2 as cv
from picamera2 import Picamera2
from libcamera import Transform
import time

# consts
FPS_POSITION = (30,60)
FPS_FONT = cv.FONT_HERSHEY_SIMPLEX
FPS_FONT_SCALE = 1.5
FPS_FONT_COLOR = (255,0,0)
FPS_THICKNESS = 3
UP=1
DOWN=0
RIGHT=1
LEFT=0
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 468
RECTANGLE_SIZE = (50, 100)
RECTANGLE_COLOR=(255,0,255)
RECTANGLE_THICKNESS=-1 # solid
MAX_HORIZONTAL_POSITION = SCREEN_WIDTH - RECTANGLE_SIZE[0]
MAX_VERTICAL_POSITION = SCREEN_HEIGHT - RECTANGLE_SIZE[1]

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
rectangle_position_start = (100,100)
rectangle_position_end = (rectangle_position_start[0] + RECTANGLE_SIZE[0], rectangle_position_start[1] + RECTANGLE_SIZE[1])
rectangle_motion_direction = (DOWN,RIGHT)

def recalculate_rectangle_position():
    global rectangle_position_start, rectangle_position_end, rectangle_motion_direction, UP, DOWN, LEFT, RIGHT, MAX_HORIZONTAL_POSITION, MAX_VERTICAL_POSITION
    (horiz_pos, vert_pos) = rectangle_position_start
    (horiz_dir, vert_dir) = rectangle_motion_direction
    if horiz_dir == RIGHT:
        horiz_pos += 5
    if horiz_dir == LEFT:
        horiz_pos -= 5
    if horiz_pos < 0:
        horiz_pos = 0
        horiz_dir = RIGHT
    if horiz_pos > MAX_HORIZONTAL_POSITION:
        horiz_pos = MAX_HORIZONTAL_POSITION
        horiz_dir = LEFT
    if vert_dir == UP:
        vert_pos -= 5
    if vert_dir == DOWN:
        vert_pos += 5
    if vert_pos < 0:
        vert_pos = 0
        vert_dir = DOWN
    if vert_pos > MAX_VERTICAL_POSITION:
        vert_pos = MAX_VERTICAL_POSITION
        vert_dir = UP
    rectangle_position_start = (horiz_pos, vert_pos)
    rectangle_position_end = (rectangle_position_start[0] + RECTANGLE_SIZE[0], rectangle_position_start[1] + RECTANGLE_SIZE[1])
    rectangle_motion_direction = (horiz_dir, vert_dir)

try:

    while True:
        tStart=time.time()
        frame=piCam.capture_array()
        recalculate_rectangle_position()
        cv.putText(frame, f"{fps:.1f}", FPS_POSITION, FPS_FONT, FPS_FONT_SCALE, FPS_FONT_COLOR, FPS_THICKNESS)
        cv.rectangle(frame, rectangle_position_start, rectangle_position_end, RECTANGLE_COLOR, RECTANGLE_THICKNESS)
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
