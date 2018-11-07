#!/usr/bin/env python
# cording : UTF-8

import serial
import rospy
from sensor_msgs.msg import *

ser=serial.Serial(
  	port = '/dev/vsrc',
   	baudrate = 115200,
 	 	parity = serial.PARITY_NONE, 
 	 	bytesize = serial.EIGHTBITS,
 	 	stopbits = serial.STOPBITS_ONE,
   	timeout = None,
   	xonxoff = 0,
   	rtscts = 0,
#   interCharTimeout = None
)

joint_name =  ["","L_wheel","R_wheel","L_shoulder_roll","L_shoulder_pitch","L_elbow_yaw","L_shoulder_pitch", "R_shoulder_roll","R_shoulder_pitch","R_elbow_yaw","R_elbow_pitch", "neck_pitch","neck_roll\t","neck_yaw\t","nouse","nouse","nouse","nouse","nouse","L_hand_yaw","L_hand_thumb","L_hand_index","L_hand_mid","L_hand_ring","L_hand_pinky","R_hand_yaw","R_hand_thumb","R_hand_index","R_hand_mid","R_hand_ring","R_hand_pinky"]


L_motion_deg = 0
R_motion_deg = 0

while True:
	try:
		print("\n1.pose_init  2.R  3.get_enc  4.gain_on  5.gain_off  6.motion 0.exit")
		command = input("select>>")
		
		if command == 1: #<pose_init>
			ser.write("@00c8:T8000:T8000:T8000:T0000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n")
			print ser.readline(),

		elif command == 2: #<R>
			ser.write("R\n")
			print ser.readline(),

		elif command == 3: #<get_enc>
			ser.write(":Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx::::::T8000:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:T8000:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx\n");
			str = ser.readline(),
			print str[0]
			position_list = str[0].split(";")
			position_list_16 = []
			position_list_10 = []

			#print str[0].split(";")
			#print "left_wheel:",position_list[1]
			
			for i in range(1,31): 
				position_list[i] = position_list[i][1:]
				#print type(position_list[i])
				#position_list[i] = hex(position_list[i])
				#print type(position_list[i])
				if len(position_list[i]) != 0:
					position_list[i] = int(position_list[i],16)
				else:
					pass
				
				#print  '%2d'%i,")", joint_name[i]	,"\t:", position_list_16[i], position_list_10[i]
				print  '%2d'%i,")", joint_name[i]	,"\t:", position_list[i]

		elif command == 4: #<gain_on>
			ser.write(":P0100:P0100:P0040:P0080:P0045:P0040:P0040:P0080:P0045:P0040:P0080:P0200:P0016::::::P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001\n")

			print ser.readline(),

		elif command == 5: #<gain_off>
			ser.write("P0000\n")
			print ser.readline(),

		elif command == 6: #<motion>
			print "\n<move wheel>"

			motion_type = input("1:panzer vor! 2:RIGHT! 3:LEFT! 4:reverse! 5:cancel>")
			if motion_type == 1:
					motion_in = input("distance of ahead!>")
					L_motion_deg += motion_in
					R_motion_deg += motion_in
					motion_time = motion_in * 0.5

			elif motion_type == 2:
					rad = input("rad of turn right!>")
					L_motion_deg += rad * 0.35
					R_motion_deg -= rad * 0.35
					motion_time = rad * 0.6

			elif motion_type == 3:
					rad = input("rad of turn left!>")
					L_motion_deg -= rad * 0.35
					R_motion_deg += rad * 0.35
					motion_time = rad * 0.6

			elif motion_type == 4:
					motion_in = input("distance of reverse!>")
					L_motion_deg -= motion_in
					R_motion_deg -= motion_in
					motion_time = motion_in * 0.8		

			elif motion_type == 5:
					break

			else: break

			print "L_motion_deg:", L_motion_deg
			print "R_motion_deg:", R_motion_deg
			print "motion_time :", motion_time

			#L_motion_deg = input("L:take in(-180~180)>")
			#R_motion_deg = input("R:take in(-180~180)>")
			
			L_wheel = 32768 + L_motion_deg * 44
			R_wheel = 32768 - R_motion_deg * 44

			print "L_wheel:", L_wheel
			print "R_wheel:", R_wheel

			L_wheel = '%x' % L_wheel
			R_wheel = '%x' % R_wheel
				
			#culculate motion_time
			motion_time *= 40
			time_16 = '%04x' %(motion_time)
			print time_16

			#cul and check motion
			print "motion_L&R_wheel"
			motion = "@"+time_16+":T"+L_wheel+":T"+R_wheel+":T8000:T0000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n"
			print motion
			ser.write("@"+time_16+":T"+L_wheel+":T"+R_wheel+":T8000:T0000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n")
			print ser.readline(),

		elif command == 0: 
			ser.close() 
			break

		elif command == "":
			ser.close()
			break

		else: 
			ser.close() 
			break

	
	except:
		print "except"
		break
		
			


