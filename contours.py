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

#FUNCTIONS
hLow = 0
hHigh = 1
sLow = 0
sHigh = 1
vLow = 0
vHigh = 1

def trackHue(val):
    global hLow
    hLow = val
    
def trackSat(val):
    global sLow
    sLow = val
    
def trackVal(val):
    global vLow
    vLow = val
def trackHhigh(val):
    global hHigh
    hHigh = val
def trackShigh(val):
    global sHigh
    sHigh = val
def trackVhigh(val):
    global vHigh
    vHigh = val

fps = 0
t2 = 0
pos = (30,60)
title = "HSV Track Bar"
cv2.namedWindow(title)
cv2.createTrackbar("Hue low",title,0,179,trackHue)
cv2.createTrackbar("Hue high",title,0,180,trackHhigh)
cv2.createTrackbar("Sat low",title,0,255,trackSat)
cv2.createTrackbar("Sat high",title,0,255,trackShigh)
cv2.createTrackbar("Val low",title,0,255,trackVal)
cv2.createTrackbar("Val high",title,0,255,trackVhigh)

while True:
    t1 = time.time()
    im = picam2.capture_array() #grab a frame
    #### To Do ....... #########
    cv2.putText(im,"fps: "+str(int(fps)),pos,cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3)
    
    #cv2.circle(im,(440,350),100,rColor,2)
    lowBound = np.array([hLow,sLow,vLow])
    highBound = np.array([hHigh,sHigh,vHigh])
    imHSV = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    mask  = cv2.inRange(imHSV,lowBound,highBound)
    smask = cv2.resize(mask,(720,520))
    objOfInterest = cv2.bitwise_and(im,im,mask=mask)
    obj = cv2.resize(objOfInterest, (520,420))
    contours,junk = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    ##cv2.findContours() returns two values
    if len(contours) > 0:
        contours = sorted(contours,key=lambda x:cv2.contourArea(x), reverse=True)
        cv2.drawContours(im,contours,0,(0,255,0),3)
        contour = contours[0]
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),3)
    #print(hLow ," ",hHigh)
    #### END 
    cv2.imshow("Camera", im)
    cv2.imshow("mask",smask)
    cv2.imshow("OBJ",obj)
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

