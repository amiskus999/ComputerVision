import cv2
from picamera2 import Picamera2
import numpy as np 
import time

picam2 = Picamera2()
#functions
xpos =0
ypos =0
wpos =0
hpos = 0
def trackX(val):
    global xpos
    xpos = val
def trackY(val):
    global ypos
    ypos = val
def trackW(val):
    global wpos
    wpos = val
def trackH(val):
    global hpos
    hpos = val
    
#do not touch this, needed for 64bit
#Picamera2 library handles the camera

picam2.preview_configuration.main.size = (920,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 60
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()



fps = 0
t2 = 0
pos = (30,60)

cv2.namedWindow("track bar")
    
cv2.createTrackbar("X Pos", "track bar",0,919,trackX)
cv2.createTrackbar("Y Pos", "track bar",0,719,trackY)
cv2.createTrackbar("box width", "track bar",0,919,trackW)
cv2.createTrackbar("box height", "track bar",0,719,trackH)
print(xpos)
while True:
    t1 = time.time()
    im = picam2.capture_array() #grab a frame
    #### To Do ....... #########
    cv2.putText(im,"fps: "+str(int(fps)),pos,cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3)
    
    #cv2.circle(im,(440,350),100,rColor,2)
    cv2.rectangle(im,(xpos,ypos),(xpos+wpos,ypos+hpos),(0,255,0),2)
    #### END 
    cv2.imshow("Camera", im)
    
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

