import cv2
from picamera2 import Picamera2
import time

piCam = Picamera2()
piCam.preview_configuration.main.size = (640,360)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.controls.FrameRate=30
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

fps=30

while True:
    tStart=time.time()
    frame=piCam.capture_array()
    cv2.putText(frame, f"{fps:.1f}", (30,60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 3)
    cv2.imshow("piCam",frame)
    if cv2.waitKey(1) == ord('q'):
        break
    tEnd=time.time()
    elapsed_time = tEnd - tStart
    fps=.99*fps + .01*(1/elapsed_time)
    #print(f"{fps:.1f}")

cv2.destroyAllWindows()
