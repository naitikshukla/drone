from VanishingPoint import *
import os
import time
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

        
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            print "Reached target altitude"
            break
        time.sleep(1)

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
	if cenx < centerx-centery/4:										#for left
		#print ("Go Right")
		print ("left and right boundaries",(centerx-centery/3,centerx+centery/3))
		txt='Left'
		loc = (xa+2,ya+(yb-ya)/2)
		cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, 1, (123,255,255), 3)
	if (cenx > centerx-centery/4 and cenx < centerx+centery/4):			# For Centre
		#print ("center")
		txt = "Center"
		loc = (xa,ya+2)
		cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,123), 3)
	if (cenx > centerx+centery/4):										# For Right
		#print ("Go Left")
		txt = "Right"
		loc = (xa,ya+2)
		cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,123,255), 3)
	#cv2.imshow("tracker", img)
	cv2.imwrite("C:/Users/naiti/Desktop/vanishingpoint/pictures/output/final.jpg", img)
	cv2.waitKey(1)
	if not txt:
		txt = "none"
	return txt
	#return img

def direction1(cell_num):
	"""
	Based on block number received from grid(between 1 to 56) we can estimate the poistion for drone to be heading towards
	here return is text where vanishing point detected , need to send copter towards that direction.
	"""
	if cell_num in [3,4,5,10,11,12,17,18,19]:
		txt = 0	#left
		#print txt
	if cell_num in [38,39,40,45,46,47,52,53,54]:
		txt = 1	#Right
		#print txt
	if cell_num in [24,25,26,31,32,33]:
		txt = 2	#Center
		#print txt
	if cell_num in [1,2,8,9,15,16]:
		txt = 5	#Top Left
		#print txt
	if cell_num in [22,23,29,30]:
		txt = 3	#Top
		#print txt
	if cell_num in [36,37,43,44,50,51]:
		txt = 6	#Top-Right
		#print txt
	if cell_num in [6,7,13,14,20,21]:
		txt = 7	#Bottom-Left
		#print txt
	if cell_num in [27,28,34,35]:
		txt = 4	#Bottom
		#print txt
	if cell_num in [41,42,48,49,55,56]:
		txt = 8	#Bottom-Right
		#print txt
	if not txt:
		txt = 99	#none
	return txt

def condition_yaw(heading, relative=False):
    """
    Send MAV_CMD_CONDITION_YAW message to point vehicle at a specified heading (in degrees).

    This method sets an absolute heading by default, but you can set the `relative` parameter
    to `True` to set yaw relative to the current yaw heading.

    By default the yaw of the vehicle will follow the direction of travel. After setting 
    the yaw using this function there is no way to return to the default yaw "follow direction 
    of travel" behaviour (https://github.com/diydrones/ardupilot/issues/2427)

    For more information see: 
    http://copter.ardupilot.com/wiki/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_condition_yaw
    """
    if relative:
        is_relative = 1 #yaw relative to direction of travel
    else:
        is_relative = 0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)

"""
Functions that move the vehicle by specifying the velocity components in each direction.
The two functions use different MAVLink commands. The main difference is
that depending on the frame used, the NED velocity can be relative to the vehicle
orientation.

The methods include:
* send_ned_velocity - Sets velocity components using SET_POSITION_TARGET_LOCAL_NED command
* send_global_velocity - Sets velocity components using SET_POSITION_TARGET_GLOBAL_INT command
"""

def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors and
    for the specified duration.

    This uses the SET_POSITION_TARGET_LOCAL_NED command with a type mask enabling only 
    velocity components 
    (http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned).
    
    Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
    with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
    velocity persists until it is canceled. The code below should work on either version 
    (sending the message multiple times does not cause problems).
    
    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 

    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

def center(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict North")
	send_ned_velocity(NORTH,0,0,DURATION)
	send_ned_velocity(0,0,0,1)

def left(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict left")
	send_ned_velocity(NORTH,WEST,0,DURATION)
	send_ned_velocity(0,0,0,1)

def right(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict right")
	send_ned_velocity(NORTH,EAST,0,DURATION)
	send_ned_velocity(0,0,0,1)

def top(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict UP")
	send_ned_velocity(NORTH,0,UP,DURATION)
	send_ned_velocity(0,0,0,1)

def bottom(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict down")
	send_ned_velocity(NORTH,0,DOWN,DURATION)
	send_ned_velocity(0,0,0,1)

def topl(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict Top Left")
	send_ned_velocity(NORTH,WEST,UP,DURATION)
	send_ned_velocity(0,0,0,1)

def topr(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict Top right")
	send_ned_velocity(NORTH,EAST,UP,DURATION)
	send_ned_velocity(0,0,0,1)

def bottoml(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict bottom Left")
	send_ned_velocity(NORTH,WEST,DOWN,DURATION)
	send_ned_velocity(0,0,0,1)

def bottomr(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict bottom right")
	send_ned_velocity(NORTH,EAST,DOWN,DURATION)
	send_ned_velocity(0,0,0,1)

def none(NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION):
	print("Velocity strict stated")
	#send_ned_velocity(NORTH,EAST,UP,DURATION)
	send_ned_velocity(0,0,0,1)
	
def main():
	#Arm and take of to altitude of 5 meters
	arm_and_takeoff(5)
	filepath = os.path.abspath("C:/Users/naiti/Desktop/vanishingpoint/pictures/input/corridor_6.jpg")
	
	img = cv2.imread(filepath)
	img = cv2.resize(img, (640, 480))
	hough_lines = hough_transform(img)
	if hough_lines:
		random_sample = sample_lines(hough_lines, 100)
		intersections = find_intersections(random_sample, img)
		for x,y in intersections:
			cv2.circle(img,(x,y), 5, (124,0,255), -1)
		cv2.imwrite("C:/Users/naiti/Desktop/vanishingpoint/pictures/output/circle.jpg", img)
		if intersections:
			grid_size = min(img.shape[0], img.shape[1]) // 9
			print img.shape[0],img.shape[1],img.shape[0]//9,grid_size
			best_cell,best_cell_num = find_vanishing_point(img, grid_size, intersections)
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
			direction_point = direction(img,rx1,ry1,rx2,ry2,img.shape[1],img.shape[0])
			direction_block = direction1(best_cell_num)
			
			# map the inputs to the function blocks
			options ={	0 : left,
						1 : right,
						2 : center,
						3 : top,
						4 : bottom,
						5 : topl,
						6 : topr,
						7 : bottoml,
						8 : bottomr,
						99: none
					 }
			
			print "Direction via point method: ", direction_point
			print "Direction via block method: ", str(options[direction_block])
			
			"""
			Code starts for drone direction heading
			
			Fly the vehicle in a SQUARE path using velocity vectors (the underlying code calls the 
			SET_POSITION_TARGET_LOCAL_NED command with the velocity parameters enabled).
			
			The thread sleeps for a time (DURATION) which defines the distance that will be travelled.
			
			The code also sets the yaw (MAV_CMD_CONDITION_YAW) using the `set_yaw()` method in each segment
			so that the front of the vehicle points in the direction of travel
			"""
			#Set up velocity vector to map to each direction.
			# vx > 0 => fly North
			# vx < 0 => fly South
			NORTH = 2
			SOUTH = -1
			
			# Note for vy:
			# vy > 0 => fly East
			# vy < 0 => fly West
			EAST = 1
			WEST = -1
			
			# Note for vz: 
			# vz < 0 => ascend
			# vz > 0 => descend
			UP = -0.5
			DOWN = 0.5
			
			DURATION = 2  # 2 secs
			
			# Calling direction functions.
			options[direction_block](NORTH,SOUTH,EAST,WEST,UP,DOWN,DURATION) 

import dronekit_sitl
sitl = dronekit_sitl.start_default()			
connection_string = sitl.connection_string()			

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)

main()
