import cv2
import time
#import roboflow
import threading
from picamera2 import Picamera2

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

import utils
model = 'efficientdet_lite0.tflite'
num_threads = 4

dispW = 920
dispH = 720
#important variables
global condition
condition = True

def timer():
    global ctr
    global im_num
    im_num = 0
    ctr = 0
    while condition:
        time.sleep(1)
        ctr += 1
        if ctr == 20:
            ctr = 0
            im_num += 1
            print("20 seconds!!!")

    #eturn "done"

picam2 = Picamera2()
picam2.preview_configuration.main.size=(dispW,dispH)
picam2.preview_configuration.main.format='RGB888'
picam2.preview_configuration.controls.FrameRate=120
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

fps=0
pos=(30,60)
font=cv2.FONT_HERSHEY_SIMPLEX
height=1.5
weight=3
myColor=(0,0,255)
#object detection
base_options = core.BaseOptions(file_name=model,use_coral=False,
                               num_threads=num_threads)
detection_options=processor.DetectionOptions(max_results=4,
                                             score_threshold=.3)
options=vision.ObjectDetectorOptions(base_options=base_options,
                                     detection_options=detection_options)
detector=vision.ObjectDetector.create_from_options(options)

#threading
timerThread = threading.Thread(target=timer)
timerThread.start()
file_name = open("pictures_log.txt","a")

while True:
    tStart=time.time()
    frame= picam2.capture_array()
    #frame=cv2.flip(frame,-1)
    #TO DO
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frameTF = vision.TensorImage.create_from_array(frameRGB)
    mydetections=detector.detect(frameTF)
    for mydetect in mydetections.detections:
        #print(mydetect.categories[0].category_name)
        if mydetect.categories[0].category_name=="cell phone":
            curr = time.ctime(time.time())
            cv2.imwrite("phone.jpg",frame)
            file_name.write(f"{curr} \t phone.jpg")
            print("phone photo saved!")

        elif mydetect.categories[0].category_name=="keyboard":
            curr = time.ctime(time.time())
            cv2.imwrite("keyboard.jpg",frame)
            file_name.write(f"{curr} \t keyboard.jpg")
            print("keyboard image saved!")
    image=utils.visualize(frame,mydetections)
    cv2.putText(frame,str(int(fps))+' FPS',pos,font,height,myColor,weight)

    if ctr == 19:
        curr = time.ctime(time.time())
        cv2.imwrite(f'testcam{im_num}.jpg',frame)
        file_name.write(f'{curr} \t testcam{im_num}.jpg')
        print("image saved after 20s")


    cv2.imshow("Camera", frame)

    if cv2.waitKey(1)==ord('q'):
        condition  = False
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)
file_name.close()
cv2.destroyAllWindows()
timerThread.join()