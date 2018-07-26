#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import rospy
import readchar
from sensor_msgs.msg import *
from sobit_model.msg import Motion_deg

ser=serial.Serial(
  		port = '/dev/ttyUSB0',
   	baudrate = 115200,
 	 	parity = serial.PARITY_NONE, 
 	 	bytesize = serial.EIGHTBITS,
 	 	stopbits = serial.STOPBITS_ONE,
   	timeout = None,
   	xonxoff = 0,
   	rtscts = 0,
#   	interCharTimeout = None
)

joint_name =  ["motion_time","L_wheel\t","R_wheel\t","L_shoulder_roll","L_shoulder_pitch","L_elbow_yaw","L_shoulder_pitch", "R_shoulder_roll","R_shoulder_pitch","R_elbow_yaw","R_elbow_pitch", "neck_pitch","neck_roll\t","neck_yaw\t", "L_hand_yaw","L_hand_thumb","L_hand_index","L_hand_mid","L_hand_ring","L_hand_pinky", "R_hand_yaw","R_hand_thumb","R_hand_index","R_hand_mid","R_hand_ring","R_hand_pinky"]

enc_name =  ["L_wheel\t","R_wheel\t","L_shoulder_roll","L_shoulder_pitch","L_elbow_yaw","L_shoulder_pitch", "R_shoulder_roll","R_shoulder_pitch","R_elbow_yaw","R_elbow_pitch", "neck_pitch","neck_roll\t","neck_yaw\t"]


###############################################################################################################
#初期設定
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



###############################################################################################################
def cul_motion(motion_deg):
		motion=[0]*21

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
		motion[7] = '%x' %(32768 + motion_deg[6] * 97)

		#<L_shoulder_pitch>
		motion[8] = '%x' %(32768 + motion_deg[7] * 86)

		#<L_elbow_yaw>
		motion[9] = '%x' %(32768 - motion_deg[8] * 58)
		
		#<L_elbow_pitch>
		motion[10] = '%x' %(32768 + motion_deg[9] * 105)

		#<neck_pitch>
		motion[11] = '%x' %(32768 + motion_deg[10] * 110)
		
		#<neck_roll>
		motion[12] = '%x' %(32768 + motion_deg[11] * 112)

		#<neck yaw>
		motion[13] = '%x' %(32768 + motion_deg[12] * 246)

		#<L_hand_twist>
		motion[14] = '%x' %(32768 - motion_deg[13] * 91)

		#<L_hand_thumb>
		motion[15] = '%x' %(32768 - motion_deg[14] * 91)

		#<L_hand_index>
		motion[16] = '%x' %(26624 - motion_deg[15] * 68)

		#<L_hand_middle>
		motion[17] = '%x' %(38912 + motion_deg[16] * 68)

		#<L_hand_ring>
		motion[18] = '%x' %(26624 - motion_deg[17] * 68)

		#<L_hand_index>
		motion[19] = '%x' %(38912 + motion_deg[18] * 68)

		#<R_hand_twist>
		motion[20] = '%x' %(32768 + motion_deg[19] * 91)

		print "<CUL_MOTION>"
		for i in range(0,21):
				print  '%2d'%i,")", joint_name[i] ,"\t:", motion[i]

		return motion


#################################################################################################################
#エンコーダ取得
def get_enc():
			print "<get_enc>"
			ser.write(":Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx::::::T8000:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx:T8000:Cxxxx:Cxxxx:Cxxxx:Cxxxx:Cxxxx\n");
			str = ser.readline(),
			print str[0]
			position_enc = str[0].split(";")

			print position_enc

			rospy.init_node('sobit_enc')
			pub_enc = rospy.Publisher('/sobit_enc', Jointstate, queue_size=10)
			enc_msg = Jointstate()
			enc_msg.name = enc_name			

			for i in range(1,21):
				enc_msg.position[i] = position_enc[i+1]
				print "enc_msg.position[" ,i, "]: ", enc_msg.position[i]

	
			pub_enc.publish(enc_msg)

			
#################################################################################################################
#モーション送受信
def callback(motion_deg):
			if motion_deg.time == 0:#時間が0の時は何も動作をしない
				return

			print "[callback]"
			
			print motion_deg , "\n"

			#モーションの計算
			motion = cul_motion(motion_deg.motion)

			#モーションタイムの計算
			time = motion_deg.time
			time *= 40
			time_16_str = '%04x' %(time)


			#モーションの送信		
			print "<MOTION_SEND>"
			print "@"+time_16_str+":T"+motion[1]+":T"+motion[2]+":T"+motion[3]+":T0000:T"+motion[5]+":T"+motion[6]+":T"+motion[7]+":T"+motion[8]+":T"+motion[9]+":T"+motion[10]+":"+motion[11] +":T"+motion[12]+":T"+motion[13]+"::::::T"+motion[14]+":T"+motion[15]+":T"+motion[16]+":T"+motion[17]+":T"+motion[18]+":T"+motion[19]+":T"+motion[20]+":T8000:T9800:T6800:T9800:T6800"

			ser.write("@"+time_16_str+":T"+motion[1]+":T"+motion[2]+":T"+motion[3]+":T0000:T"+motion[5]+":T"+motion[6]+":T"+motion[7]+":T"+motion[8]+":T"+motion[9]+":T"+motion[10]+":T"+motion[11] +":T"+motion[12]+":T"+motion[13]+"::::::T"+motion[14]+":T"+motion[15]+":T"+motion[16]+":T"+motion[17]+":T"+motion[18]+":T"+motion[19]+":T"+motion[20]+":T8000:T9800:T6800:T9800:T6800\n")
			print ser.readline(),


####################################################################################################################
#メイン関数
if __name__ == '__main__':
			#初期設定			
			first_set()
			print "If you want to end this program, push 'q' key!"
	
			#処理ループ
			while True:
				#エンコーダの読み込み
				#get_enc()

				rospy.sleep(1)

				#モーション送受信
				rospy.init_node('output_state', anonymous=True)
				sub = rospy.Subscriber('/motion_deg', Motion_deg, callback)

	
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

				
				 








