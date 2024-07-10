import cv2
import time
#import roboflow
from picamera2 import Picamera2

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

import utils
model = 'efficientdet_lite0.tflite'
num_threads = 4

dispW = 920
dispH = 720

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
detection_options=processor.DetectionOptions(max_results=8,
                                             score_threshold=.3)
options=vision.ObjectDetectorOptions(base_options=base_options,
                                     detection_options=detection_options)
detector=vision.ObjectDetector.create_from_options(options)
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
            cv2.imwrite("phone.jpg",frame)
            print("phone photo saved!")
        elif mydetect.categories[0].category_name=="keyboard":
            cv2.imwrite("keyboard.jpg",frame)
            print("keyboard image saved!")
    image=utils.visualize(frame,mydetections)
    cv2.putText(frame,str(int(fps))+' FPS',pos,font,height,myColor,weight)
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1)==ord('q'):
        break
    tEnd=time.time()
    loopTime=tEnd-tStart
    fps=.9*fps + .1*(1/loopTime)
cv2.destroyAllWindows()