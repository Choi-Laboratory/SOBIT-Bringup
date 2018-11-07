#!/usr/bin/env python
# cording : UTF-8

import serial
import rospy
import sys
from sensor_msgs.msg import *

def callback():
	while True:
		print("")
		key_in = raw_input("push key WASD>>")

		if 'w' in key_in: #up
			print("ue")

		elif 's' in key_in: #down
			print("shita")

		elif key_in == 'd': #right
			print("migi")

		elif key_in == 'a': #left
			print("hidari")

		elif key_in == 'o': #out
			print("out")
			break	


if __name__ == '__main__':
	print("teleop_test")

	#rospy.init_node('velocity', anonymous=True)
	
	callback()
	
	rospy.sleep(0.1)

	rospy.spin()
