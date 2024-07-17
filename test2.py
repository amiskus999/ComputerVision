import cv2
from picamera2 import Picamera2
import time

#do not touch this, needed for 64bit
#Picamera2 library handles the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (920,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 60
picam2.preview_configuration.align()
picam2.configure("preview")

def changePos(p1,p2):
    delta = 1
    if ((p1[0]+delta) < 0) | ((p2[0]+delta) > 919):
        delta *= (-1)
    if ((p1[1]+delta) < 0) | ((p2[1]+delta) > 719):
        delta *= (-1)
    return delta

picam2.start()

fps = 0
t2 = 0
 
pos = (30,60)
tlc = 240
tlr = 200
llc = 640
llr = 400
rColor = (0,125,0)
rThick = -1
deltaR = 5
deltaC = 5

while True:
    t1 = time.time()
    im = picam2.capture_array() #grab a frame
    #### To Do ....... #########
    
    ## display text on video
    #pos = changePos(pos)
    if ((tlc+deltaC) < 0) | ((llc+deltaC) > 919):
        deltaC *= (-1)
        
    if ((tlr+deltaR) < 0) | ((llr+deltaR) > 719):
        deltaR *= (-1)
    llr += deltaR
    tlr += deltaR   
    tlc += deltaC
    llc += deltaC
    upLeft = (tlc,tlr)
    lowRight = (llc,llr)
    
    cv2.putText(im,"fps: "+str(int(fps)),pos,cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3)
    
    cv2.rectangle(im,upLeft,lowRight,rColor,rThick)
    #cv2.circle(im,(440,350),100,rColor,2)
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
