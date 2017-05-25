from VanishingPoint import *
import os
import time

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
	cv2.circle(img, (centerx,centery), 4, (0,0,123), thickness=3, lineType=7, shift=0)	#Screen centre
	cv2.circle(img, (cenx,ceny), 4, (0,232,123), thickness=1, lineType=7, shift=0)	#new box centre
	cv2.rectangle(img, (int(centerx-centery/4), centery+centerx/5), (int(centerx+centery/4), centery-centerx/5), (255, 123, 11), 3)		#range rectangle
	#cv2.rectangle(img, (xa,ya), (xb,yb), (34, 123, 145), 1)			#Object rectangle
	
	#if time.time() > timeout:
	#	break
	if cenx < centerx-centery/4:						#for left
		print ("Go Right")
		print ("left and right boundaries",(centerx-centery/3,centerx+centery/3))
		txt='Left'
		loc = (xa+2,ya+(yb-ya)/2)
		cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, 1, (123,255,255), 3)
	if (cenx > centerx-centery/4 and cenx < centerx+centery/4):			# For Centre
		print ("center")
		txt = "Center"
		loc = (xa,ya+2)
		cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,123), 3)
	if (cenx > centerx+centery/4):			# For Right
		print ("Go Left")
		txt = "Right"
		loc = (xa,ya+2)
		cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,123,255), 3)
	#cv2.imshow("tracker", img)
	cv2.imwrite("C:/Users/naiti/Desktop/vanishingpoint/pictures/output/final.jpg", img)
	cv2.waitKey(1)
	#return img

filepath = os.path.abspath("C:/Users/naiti/Desktop/vanishingpoint/pictures/input/corridor_6.jpg")

img = cv2.imread(filepath)
hough_lines = hough_transform(img)
if hough_lines:
    random_sample = sample_lines(hough_lines, 100)
    intersections = find_intersections(random_sample, img)
    for x,y in intersections:
        cv2.circle(img,(x,y), 5, (124,0,255), -1)
	cv2.imwrite("C:/Users/naiti/Desktop/vanishingpoint/pictures/output/circle.jpg", img)
    if intersections:
		grid_size = min(img.shape[0], img.shape[1]) // 3
		print img.shape[0],img.shape[1],img.shape[0]//3,grid_size
		best_cell = find_vanishing_point(img, grid_size, intersections)
		#print vanishing_point[0],vanishing_point[1]
		rx1 = best_cell[0] - grid_size / 2
		ry1 = best_cell[1] - grid_size / 2
		rx2 = best_cell[0] + grid_size / 2
		ry2 = best_cell[1] + grid_size / 2
		cv2.circle(img,(rx1,ry1), 5, (124,111,255), 2)		#left point on best cell
		cv2.circle(img,(rx2,ry2), 5, (124,111,255), 2)		# right point on best cell
		cv2.circle(img,(best_cell[0],best_cell[1]), 5, (124,111,255), 2)		# centre point on best cell
		#cv2.imshow("vanishing_point",best_cell)
		#cv2.waitKey(10)
		filename = "C:/Users/naiti/Desktop/vanishingpoint/pictures/output/corridor_6.jpg"
		cv2.imwrite(filename, img)
		direction(img,rx1,ry1,rx2,ry2,img.shape[1],img.shape[0])
