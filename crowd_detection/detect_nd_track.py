#This demo will detect for human in the frame untill it not found any human it will find repeatedly
# once box is locked it will track the human in the frame.

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
	pt1 = (int(rect.left()), int(rect.top()))
	pt2 = (int(rect.right()), int(rect.bottom()))
	cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
	#print ("Object tracked at [{}, {}] \r").format(pt1, pt2),
	cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
	cv2.imshow("Image", img)
	#if time.time() > timeout:
	#	break

	
if __name__ == "__main__":
	source =0
	cam = WebcamVideoStream(src=0).start()
	# initialize the HOG descriptor/person detector
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
	#Create the tracker object
	tracker = dlib.correlation_tracker()
	while (True):
		points=[]
		timeout = time.time() + 5
		while True:
			try:
				timeout = time.time() + 5
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
				obj_tracker(points,img)
				cv2.waitKey(1)
				if time.time() > timeout:
					del points[:]
					break
			except (KeyboardInterrupt, SystemExit):
				raise
			#except:
			#	print("some other error occured")
			#	break
	cv2.destroyAllWindows()
	cam.stop()
