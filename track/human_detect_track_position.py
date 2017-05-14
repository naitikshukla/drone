# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils				# need to install first sudo pip install imutils
from imutils.video import WebcamVideoStream
import cv2
import time 
import dlib					# need to install through binaries

def direction(img,xa,ya,xb,yb,width,height):
	#xa,ya,xb,yb=point[0],point[1],point[2],point[3]
	cenx = xa+(xb-xa)/2
	ceny = ya+(yb-ya)/2
	centerx=width/2
	centery = height/2
	timeout = time.time() + 5
	#while True:
	#_,img = cam.read()
	print("image center are :", centerx,centery)
	#img=cv2.blur(img, (3,3))
	cv2.circle(img, (centerx,centery), 4, (0,0,123), thickness=1, lineType=7, shift=0)	#Screen centre
	cv2.circle(img, (cenx,ceny), 4, (0,232,123), thickness=1, lineType=7, shift=0)	#new box centre
	cv2.rectangle(img, (int(centerx-centery/3), centery+centerx/3), (int(centerx+centery/3), centery-centerx/3), (0, 123, 432), 1)		#range rectangle
	cv2.rectangle(img, (xa,ya), (xb,yb), (34, 123, 145), 1)			#Object rectangle
	
	#if time.time() > timeout:
	#	break
	if cenx < centerx-centery/3:						#for left
		print ("inside left loop")
		print ("left and right boundaries",(centerx-centery/3,centerx+centery/3))
		txt='Left'
		loc = (xa+2,ya+(yb-ya)/2)
		cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, 1, (123,255,255), 1)
	if (cenx > centerx-centery/3 and cenx < centerx+centery/3):			# For Centre
		print ("inside center")
		txt = "Center"
		loc = (xa,ya+2)
		cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,123), 1)
	if (cenx > centerx+centery/3):			# For Right
		
		txt = "Right"
		loc = (xa,ya+2)
		cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,123,255), 1)
	cv2.imshow("tracker", img)
	cv2.waitKey(1)
	#return img
	
def humandetect(image):
	startTime = time.time()
	orig = image.copy()

	# detect people in the image
	#(rects, weights) = hog.detectMultiScale(image, winStride=(3, 4), padding=(8, 8), scale=1.07)
	(rects, weights) = hog.detectMultiScale(image, winStride=(8, 8), padding=(32, 32), scale=1.05)

	# draw the original bounding boxes
	for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.5)
	
	points=[]
	# draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
		points.append((xA,yA,xB,yB))

	# show some information on the number of bounding boxes
	#filename = imagePath[imagePath.rfind("/") + 1:]
	print("[INFO] : {} original boxes, {} after suppression".format(len(rects), len(pick)))
	text = "{} People".format(len(pick))

	# Write some Text
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(image,text,(10,50), font, .5,(255,255,255),2)

	# show the output images
	cv2.imshow("Before NMS", orig)
	cv2.imshow("After NMS", image)
	cv2.waitKey(1)
	print ("points sent: {}".format(points))
	print ('The script took {0} second !'.format(time.time() - startTime))
	return points
	
def obj_tracker(points,image):
	if not points:
		return
	# Update the tracker  
	tracker.update(img)
	# Get the position of the object, draw a 
	# bounding box around it and display it.
	rect = tracker.get_position()
	
	#for directions
	xa=int(rect.left())
	ya=int(rect.top())
	xb=int(rect.right())
	yb=int(rect.bottom())
	#points for rectangle
	pt1 = (xa, ya)		#top left
	pt2 = (xb, yb)		#bottom right
	
	#call direction to plot track rectangle and find actions
	direction(img,xa,ya,xb,yb,500,500)
	#cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
	#print ("Object tracked at [{}, {}] \r").format(pt1, pt2),
	#cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
	#cv2.imshow("tracker", img)
	#if time.time() > timeout:
	#	break


	
if __name__ == "__main__":
	source =0
	cam = WebcamVideoStream(src=0).start()
	#width1 = int(cam.get(3))   # float
	#height1 = int(cam.get(4)) # float
	# initialize the HOG descriptor/person detector
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
	#Create the tracker object
	tracker = dlib.correlation_tracker()
	while (True):
		points=[]
		timeout = time.time() + 10
		while True:
			try:
				#timeout = time.time() + 3
				img = cam.read()
				img = imutils.resize(img, width=min(500, img.shape[1]))
				#points,image = humandetect()
				if not points:
					# Initial co-ordinates of the object to be tracked
					points = humandetect(img)
					if points:
						# Provide the tracker the initial position of the object
						tracker.start_track(img, dlib.rectangle(*points[0]))
						cv2.destroyAllWindows()
					continue
				cv2.namedWindow("tracker", cv2.WINDOW_NORMAL)
				#img = direction(img,points[0],500,500)
				obj_tracker(points,img)
				if time.time() > timeout:
					del points[:]
					cv2.destroyAllWindows()
					break
				##if cv2.waitKey() == 27:
				##	break
			except (KeyboardInterrupt, SystemExit):
				raise
			#except:
			#	print("some other error occured")
			#	break
	cv2.destroyAllWindows()
	cam.stop()
	
