from VanishingPoint import *
import os

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
		cv2.imshow("vanishing_point",best_cell)
		cv2.waitKey(10)
		filename = "C:/Users/naiti/Desktop/vanishingpoint/pictures/output/corridor_6.jpg"
		cv2.imwrite(filename, img)
