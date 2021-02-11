#!/usr/bin/python

import jetson.inference
import jetson.utils

import argparse
import sys

import cv2
import numpy as np
import time


# load the object detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold = 0.5)
#Change object detection: pednet, multiped, ssd-mobilenet-v1, ssd-mobilenet-v2, ssd-inception-v2

def gstreamer_pipeline (capture_width=320, capture_height=240, display_width=320, display_height=240, framerate=30, flip_method=0):   
    return ('nvarguscamerasrc ! ' 
    'video/x-raw(memory:NVMM), '
    'width=(int)%d, height=(int)%d, '
    'format=(string)NV12, framerate=(fraction)%d/1 ! '
    'nvvidconv flip-method=%d ! '
    'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! '
    'videoconvert ! '
    'video/x-raw, format=(string)BGR ! appsink'  %(capture_width,capture_height,framerate,flip_method,display_width,display_height))

#If the images are from files
#cap = cv2.VideoCapture('./img (%d).bmp')

cap = cv2.VideoCapture(0) #usb cam

ret = True
fcount = 0

while ret:
	# capture the image	
	start = time.time()
	ret, img = cap.read()

	w = 320
	h = 240 

	img = cv2.resize(img, (w, h))	
	
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA).astype(np.float32) #convert to RGBA with 32-bit float numbers
	img = jetson.utils.cudaFromNumpy(img)

	detections = net.Detect(img, w, h)

	img = jetson.utils.cudaToNumpy(img, w, h, 4)
	img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB).astype(np.uint8) #back to OpenCV-format (BGR with 8-bit ints)
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    #For some object only, such as human detection
    #Human class id = 1
    #For pednet and multiped no need this

	for i in range(len(detections)):
		if detections[i].ClassID == 1:
			startX = int(detections[i].Left)
			startY = int(detections[i].Top)
			endX = int(detections[i].Right)
			endY = int(detections[i].Bottom)

    
	fcount += 1

	fps = 1.0/(time.time()-start)
	print("FPS: ", fps)

	cv2.putText(img, "FPS : " + str(fps), (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
	
	cv2.imshow('Object Detection', img)
	#cv2.imwrite('img_' + str(fcount) + '.jpg', img)

	if cv2.waitKey(1) & 0xFF == ord('c'):
        break
