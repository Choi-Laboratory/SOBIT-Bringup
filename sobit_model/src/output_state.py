#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import rospy
import sys
import roslib.packages
from sensor_msgs.msg import *
from sobit_model.msg import Motion_deg

file_path = roslib.packages.get_pkg_dir('sobit_model') + "/motion/"
out_file_name = raw_input("output file's name >> ")
out_file = open(file_path + out_file_name + '.txt', 'w')  #書き込みモードでオープン
save_flag = False
close_flag = False
motion_time = 0.0

def callback(motion_deg):
	global save_flag , out_file , close_flag , motion_time

	if save_flag == True:	
		motion_deg.time = motion_time
		string = str(motion_deg) 
		print string
		out_file.write(string)
		out_file.write("\n")
		save_flag = False
	elif close_flag == True:
		print "ok saved motions"
		out_file.close()
		close_flag = False


if __name__ == '__main__':
	
	rospy.init_node('output_state', anonymous=True)
	sub = rospy.Subscriber('motion_deg', Motion_deg, callback)
	
	while True:
		print ""
		key_in = raw_input("push 'q'key to save motion_deg, or 'c'key to close >> ")
		if key_in == "q":
			motion_time = raw_input("motion time? >>")
			save_flag = True
		elif key_in == "c":
			close_flag = True
			break
		rospy.sleep(0.1)
	rospy.spin()
	
