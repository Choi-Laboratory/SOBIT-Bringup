#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import rospy
import readchar
import math
from sensor_msgs.msg import *
from geometry_msgs.msg import Twist

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

#グローバル関数
L_motion_deg = 0
R_motion_deg = 0

####初期設定####################################################################################################
def first_set():
		print "[First_set]"

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



####cul_motion##############################################################################################
def cul_wheel(vel,ang):
	global L_motion_deg
	global R_motion_deg
	motion = [0]*3
	motion_in = 0
	time = 0.1

	#単位時間あたりの移動距離
	print "vel:",+vel 	#vel:速度[m/s]
	print "ang:",+ang 	#ang:角速度[rad/s]
	print "time:",+time 	#time:単位時間[s]

	motion_in = vel
	motion_ang = (ang * 180 /math.pi) * 0.35
	print "motion_in:",+motion_in
	  
	#モーションの計算
	if ang == 0: #前後直進
			L_motion_deg += motion_in
			R_motion_deg += motion_in

	elif ang < 0: #右回転
			L_motion_deg += motion_in
			L_motion_deg += motion_ang
			R_motion_deg += motion_in
			R_motion_deg -= motion_ang

	elif ang > 0: #左回転
			L_motion_deg += motion_in
			L_motion_deg -= motion_ang
			R_motion_deg += motion_in
			R_motion_deg += motion_ang

	#初期化
	motion_in = 0
	vel = 0

	print L_motion_deg
	print R_motion_deg

	#10→16進
	motion[0] = '%04x' %(time * 40)
	motion[1] = '%x' %(32768 + L_motion_deg * 44)
	motion[2] = '%x' %(32768 - R_motion_deg * 44)
	

	return motion


####callback########################################################################################################
def callback(cmd_vel):
	#0の時は何もしない
	if cmd_vel.linear.x == 0 and cmd_vel.angular.z == 0:
		return
	
	#速度から距離とモーションタイムを計算
	motion = cul_wheel(cmd_vel.linear.x,cmd_vel.angular.z)

	#モーションの送信		
	print "[MOTION_SEND]"
	print motion
	ser.write("@"+motion[0]+":T"+motion[1]+":T"+motion[2]+":T8000:T0000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n")
	print ser.readline(),
	rospy.sleep(0.1)
	return




####メイン関数########################################################################################################
if __name__ == '__main__':
	#初期設定			
	first_set()

	print "If you want to end this program, push 'q' key!"

	while True:

		#cmd_velの読み込み
		rospy.init_node('sobit_telecon', anonymous=True)
		sub = rospy.Subscriber('cmd_vel_mux/input/teleop', Twist, callback)

		rospy.spin()

		#キー入力(q)で終了
		kb = readchar.readchar()
		if kb == "q":
				print("[exit program]")
				print "<pose_init>"	
				ser.write("@00c8:T8000:T8000:T8000:T0000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n")
				print ser.readline(),
				rospy.sleep(3)

				print "<gain_off>"
				ser.write("P0000\n")
				print ser.readline(),

				break

				
				 



