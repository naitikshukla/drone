Sno | File Name | Description
--- | --------- | -----------
1 | **VanishingPoint.py** | which contains all the functions defined in it for detecting lines and intersection and finding grid with max intersection.
2 | **Main.py** | Python code which will call previos functions and utilize it for movement of drone.

This Folder is for Vanishing point based navigation of drone.

It contains above 2 files.

# Steps in Transform
<p>Green box defines selected grid and center,left and right points in grid.</p><br>

| Step  | Output | Details
| ------------- | ------------- | ------------- |
| 1  | <img src="/vanish_point/input.jpg" width="300">  | Input Image |
| 2  | <img src="/vanish_point/opening.jpg" width="300">  | morphologyEx Image (erode, then dilate) |
| 3  | <img src="/vanish_point/canny.jpg" width="300">  | Canny edge detection |
| 4  | <img src="/vanish_point/hough.jpg" width="300">  | Hough Transformation |
| 5  | <img src="/vanish_point/circle.jpg" width="300">  | Finding Intersection |
| 6  | <img src="/vanish_point/corridor_6.jpg" width="300">  | Finding final grid with maximum intersection |
| 7  | <img src="/vanish_point/final.jpg" width="300">  | Image for direction input given to drone |
<br>
**Code is working condition but detail for movement will be updated in time**
