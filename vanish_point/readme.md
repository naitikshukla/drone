Sno | File Name | Description
--- | --------- | -----------
1 | **VanishingPoint.py** | which contains all the functions defined in it for detecting lines and intersection and finding grid with max intersection.
2 | **Main.py** | Python code which will call previos functions and utilize it for movement of drone.

This Folder is for Vanishing point based navigation of drone.

It contains above 2 files.

# Output
<p>Green box defines selected grid and center,left and right points in grid.</p>
</n>
</n>
| Step  | Output  | Details  |
| ----- | ------- | -------- |
| 1 | blam | Input Image |
| 2 | <img src="/vanish_point/opening.jpg" width="250"> | morphologyEx Image (erode, then dilate) |
| 3 | <img src="/vanish_point/canny.jpg" width="250"> | Canny edge detection |
| 4 | <img src="/vanish_point/hough.jpg" width="250"> | Hough Transformation |
| 5 | <img src="/vanish_point/circle.jpg" width="250"> | Finding Intersection |
| 6 | <img src="/vanish_point/corridor_6.jpg" width="250"> | Finding final grid with maximum intersection |


| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

**Code is working condition but detail for movement will be updated in time**
