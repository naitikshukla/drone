# drone
All the codes working on drone for ISS-KE
This code will take latLong and any extra sensors data from drone (in my case humidity,temperature and altitude) and plot path with points on map.
Also with right click we can have extra markers in increment order from A to Z , which further we can utilize for waypoint navigation( functionality needs to add)

This code is all in python which internally converts everything to javascript and send data to Google maps API to see map.(Obviously requires Internet connection)
##################################################
Added new modified file for pointing on maps which can be used to replace earlier file MapPoints.py

What this file will do , it will have 3 csv files for operation.

1- Master File : data.csv
2- Target File : data1.csv
3- Temp File   : temp-data.csv    <- It will be used for plotting into graphs

So our Master file is realtime updating file , it has continous input values.
So when our code will run It will check difference in files between Master and Target, If it found any difference,
  It will copy the data into Temp file to create map.
  Once it create map from temp file it will append temp data into Target File ,so next time these coordinates won't come for reprocessing or plotting into maps.
  
###################################
Limitation::

This code currently have small limitation that waypoints map on this map is not continous for incrementally gather data.
Points which are collected at 1 run have connected points and other session won't be connected. There are possible two approaches can be followed :

1.  If your input data is very frequent lets say points are almost overlapping then it won't be of much issue in looking for tracking path.

2. Other approach is to add into code , store last latLong from each session into variable and when next session points will come just add last stored variable on top.
######################################

Also data.csv to work on this extend code Header values need to be removed

######################################
