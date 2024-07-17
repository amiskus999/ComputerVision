import cv2
print(cv2.__version__)
#dispW=920
#dispH=200

cam = cv2.VideoCapture('/dev/video0')
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while (True):
	ret,frame = cam.read()
	cv2.imshow('frame',frame)

	if cv2.waitKey(1) == ord('q'):
		break
cam.release()
cv2.destroyAllWindows()
