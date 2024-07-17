import cv2
from picamera2 import Picamera2
import numpy as np 
import time

#do not touch this, needed for 64bit
#Picamera2 library handles the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (920,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 60
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

fps = 0
t2 = 0
pos = (30,60)
#parameters for image to track
hLow = 100
hHigh = 110
satLow = 200
satHigh = 270
vLow = 110
vHigh = 190

lowBound = np.array([hLow,satLow,vLow])
highBound = np.array([hHigh,satHigh,vHigh])

while True:
    t1 = time.time()
    im = picam2.capture_array() #grab a frame
    #### To Do ....... #########
    cv2.putText(im,"fps: "+str(int(fps)),pos,cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3)
    imHSV = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    interest = imHSV[460,360]
    mask = cv2.inRange(imHSV,lowBound,highBound)
    objectOfInterest = cv2.bitwise_and(im,im, mask=mask)
    smask = cv2.resize(mask,(720,520))
    obj = cv2.resize(objectOfInterest, (520,420))
    print(interest)
    #cv2.circle(im,(440,350),100,rColor,2)
    #### END 
    cv2.imshow("Camera", im)
    cv2.imshow("tacker", smask)
    cv2.imshow("interest", obj)
    t2 = time.time()
    diff = t2-t1
    fps = 0.9*fps + 0.1*(1/diff)
    
    key = cv2.waitKey(1) #wait for user input
    if key==ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("cap1.jpg",im)
        print("image saved")
        break
picam2.stop()
picam2.close()
cv2.destroyAllWindows()
