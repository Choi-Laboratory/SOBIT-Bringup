#!/usr/bin/python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import *

def callback(joint):
	print joint.position
	

 
def joint_read():
	rospy.init_node('joint_state_publisher', anonymous=True)
	sub = rospy.Subscriber('joint_states', JointState, callback)
	rospy.spin()


if __name__ == '__main__':
    joint_read()
