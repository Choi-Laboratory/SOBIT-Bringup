#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import rospy
from sensor_msgs.msg import *

ser=serial.Serial(
  		port = '/dev/ttyUSB0',
   	baudrate = 115200,
 	 	parity = serial.PARITY_NONE, 
 	 	bytesize = serial.EIGHTBITS,
 	 	stopbits = serial.STOPBITS_ONE,
   	timeout = None,
   	xonxoff = 0,
   	rtscts = 0,
#   interCharTimeout = None
)

joint_name =  ["motion_time","L_wheel\t","R_wheel\t","L_shoulder_roll","L_shoulder_pitch","L_elbow_yaw","L_shoulder_pitch", "R_shoulder_roll","R_shoulder_pitch","R_elbow_yaw","R_elbow_pitch", "neck_pitch","neck_roll\t","neck_yaw\t","nouse","nouse","nouse","nouse","nouse", "L_hand_yaw","L_hand_thumb","L_hand_index","L_hand_mid","L_hand_ring","L_hand_pinky", "R_hand_yaw","R_hand_thumb","R_hand_index","R_hand_mid","R_hand_ring","R_hand_pinky"]


###############################################################################################################
def cul_motion(motion_deg):
		motion=[0]*14

		#<L_wheel>
		motion[1] = '%x' %(32768 + motion_deg[0] * 44)

		#<R_wheel>
		motion[2] = '%x' %(32768 - motion_deg[1] * 44)

		#<L_shoulder_roll>
		motion[3] = '%x' %(32768 + motion_deg[2] * 97)
		
		#<L_shoulder_pitch>
		#motion[4] = '%x' %(32768 + motion_deg[3] * 86)

		#<L_elbow_yaw>
		motion[5] = '%x' %(32768 + motion_deg[4] * 58)
		
		#<L_elbow_pitch>
		motion[6] = '%x' %(32768 + motion_deg[5] * 105)

		#<R_shoulder_roll>
		motion[7] = '%x' %(32768 - motion_deg[6] * 97)

		#<L_shoulder_pitch>
		motion[8] = '%x' %(32768 - motion_deg[7] * 86)

		#<L_elbow_yaw>
		motion[9] = '%x' %(32768 - motion_deg[8] * 58)
		
		#<L_elbow_pitch>
		motion[10] = '%x' %(32768 - motion_deg[9] * 105)

		#<neck_pitch>
		motion[11] = '%x' %(32768 + motion_deg[10] * 110)
		
		#<neck_roll>
		motion[12] = '%x' %(32768 + motion_deg[11] * 112)

		#<neck yaw>
		motion[13] = '%x' %(32768 + motion_deg[12] * 246)

		print "<CUL_MOTION>"
		for i in range(0,14):
				print  '%2d'%i,")", joint_name[i] ,"\t:", motion[i]

		return motion


###############################################################################################################
def callback(joint):
		motion_rad = ["0.0","0.0","0.0","0.0","0.0","0.0", "0.0","0.0","0.0","0.0", "0.0","0.0","0.0"]
		motion_deg = ["0.0","0.0","0.0","0.0","0.0","0.0", "0.0","0.0","0.0","0.0", "0.0","0.0","0.0"]

		print "\n<READ_JOINT_STATES>"
		#print joint.position;####

		#生データ参照
		#for i in range(0,13):
			#print  '%2d'%i,")", joint_name[i]	,"\t:", joint.position[i]
 		
		##radとdegの計算と出力
		for i in range(1,14):
				motion_deg[i-1] = joint.position[i-1] / 3.1415 * 180
				print  '%2d'%i,")", joint_name[i]	,"\tdeg:", '%3d'%motion_deg[i-1], "\trad:", joint.position[i-1]  


		motion = cul_motion(motion_deg)

		print "<MOTION>"
		print motion

		#モーションの送信		
		print "<MOTION_SEND>"
		#print "@00c8:T"+motion[1]+":T"+motion[2]+":T"+motion[3]+":T0000:T"+motion[5]+":T"+motion[6]+":T"+motion[7]+":T"+motion[8]+":T"+motion[9]+":T"+motion[10]+":"+motion[11] +":T"+motion[12]+":T"+motion[13]+"::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800"
		#rospy.sleep(0.1)
		ser.write("@0011:T"+motion[1]+":T"+motion[2]+":T"+motion[3]+":T0000:T"+motion[5]+":T"+motion[6]+":T"+motion[7]+":T"+motion[8]+":T"+motion[9]+":T"+motion[10]+":T"+motion[11]+":T"+motion[12]+":T"+motion[13]+"::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n")	
		print ser.readline(),


		#get_enc
		#rospy.sleep(0.1)
		#print "\n<get_enc>"
		#ser.write(":Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx::::::T8000:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:T8000:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx\n");
		#str = ser.readline(),
		#print str[0]
		#position_enc = str[0].split(";")
		
		#for k in range(1,14): 
			#position_enc[k] = position_enc[k][1:] ##先頭位置の文字を削除

			#if len(position_enc[k]) != 0:
			#	position_enc[k] = int(position_enc[k],16) ##16進数→10進数
			#else:
			#	pass
			#print  '%2d'%k,")", full_joint[k]	,"\t:", position_enc[k]



###############################################################################################################
#Jointstateの読み込み
def joint_read():
		print "Joint_read"
		rospy.init_node('joint_state_publisher', anonymous=True)
		sub = rospy.Subscriber('joint_states', JointState, callback)
		rospy.spin()

###############################################################################################################
#初期設定
def first_set():
			print "First_set"

			print "<pose_init>"	
			ser.write("@00c8:T8000:T8000:T8000:T0000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n")
			print ser.readline(),
			rospy.sleep(1)

			print "<R>"
			ser.write("R\n")
			print ser.readline(),
			rospy.sleep(1)

			print "<get_enc>"
			ser.write(":Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx::::::T8000:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:T8000:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx\n");
			print ser.readline(),
			rospy.sleep(1)

			print "<gain_on>"
			ser.write(":P0100:P0100:P0040:P0080:P0045:P0040:P0040:P0080:P0045:P0040:P0080:P0200:P0016::::::P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001:P0001\n")
			print ser.readline(),
			rospy.sleep(1)



###############################################################################################################
#メイン関数
if __name__ == '__main__':
			#初期設定			
			first_set()
	
			#Jointstateの読み込み
			joint_read()



			print "<pose_init>"	
			ser.write("@00c8:T8000:T8000:T8000:T0000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n")
			print ser.readline(),
			rospy.sleep(3)

			print "<gain_off>"
			ser.write("P0000\n")
			print ser.readline(),
	

