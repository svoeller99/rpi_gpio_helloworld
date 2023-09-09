import cv2
from picamera2 import Picamera2
import time

piCam = Picamera2()
piCam.preview_configuration.main.size = (1280,720)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

prior_second = time.time()
fps = 0
current_fps = 0

while True:
    frame=piCam.capture_array()
    current_fps += 1
    if time.time() - prior_second >= 1:
        fps = current_fps
        current_fps = 0
        prior_second = time.time()
        print(f"FPS: {fps}")
    cv2.imshow("piCam",frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
