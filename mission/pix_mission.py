######################################################################################################
## File created on 31-03-2016 to be used in creating waypoint mission file for Pixhawk FC			##
## By Naitik Shukla fir ISS-Drone																	##
## Sample file taken from http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format	##
######################################################################################################
list1 = [(123,456),(234,567),(345,678)]			# will be coming from android ,obile device in this format
version = '1.1'									# version of firmware currently in use

#need to be change for path
missionFile = 'C:\\Users\\naiti\\Desktop\\mission.txt'	# name of mission file and path which will be sent to pixhawk

altitude = 10									# Altitude at which drone will be flying can be get from mobile device
f = open(missionFile,"w")						#open a file in write mode
f.write('QGC\tWPL\t%s\n' % version)				# write first line for waypoint file
listLen = len(list1)							# getting length of waypoints gather in list

# Loop for all point which will be print in each line
for i in range(listLen):
	lat = list1[i][0]
	long = list1[i][1]
	f.write('%d\t1\t0\t16\t0.14999999999999994\t0\t0\t0\t%.17f\t%.17f\t%d\t1\n' % (i,lat, long, altitude))
f.close()										# close the file after write completes
