#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import rospy
import roslib.packages
from sensor_msgs.msg import *
from sobit_model.msg import Motion_deg


file_path = roslib.packages.get_pkg_dir('sobit_description') + "/motion/"
file = open( file_path + 'touth.txt','r')
string = file.readlines()

print(string)

print string[0]
print string[1]

i=0

length = len(string)
print length

rospy.init_node('motion_deg')

pub_motion_deg = rospy.Publisher('/motion_deg', Motion_deg, queue_size=10)#,latch=True
motion_deg_msg = Motion_deg()
pub_motion_deg.publish(motion_deg_msg)#最初はカラのトピックを出して通信ができる状態にさせる

while True:
		#偶数ならtime
		if i%2==0:
			string[i] = string[i][7:]
			string[i] = string[i][:-2]
			print "time: " , string[i]

		#奇数ならmotion
		elif i%2==1:
			string[i] = string[i][9:]
			string[i] = string[i][:-2]
			motion_deg_str = string[i].split(",")
			motion_deg = []
			for temp_str in motion_deg_str:
				motion_deg.append(float(temp_str))
			print "motion_deg: ", 
			print string[i]
			print "motion_deg_2: ",
			print motion_deg	



			#モーションのpublish
			print "\n<publish>"
			motion_deg_msg = Motion_deg()
			motion_deg_msg.motion = motion_deg
			motion_deg_msg.time = float(string[i-1])
			print motion_deg_msg
			pub_motion_deg.publish(motion_deg_msg)

			#rospy.sleep(0.1)
			#pub_motion_deg.publish(motion_deg_msg)

		i+=1
		rospy.sleep(1)

		#EOFで終了
		if i>=length:
			break
		

print "A"


