#!/usr/bin/env python
# cording : UTF-8

import serial

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

joint_name =  ["","L_wheel","R_wheel","L_shoulder_roll","L_shoulder_pitch","L_elbow_yaw","L_shoulder_pitch", "R_shoulder_roll","R_shoulder_pitch","elbow_yaw","R_elbow_pitch", "neck_pitch","neck_roll\t","neck_yaw\t","nouse","nouse","nouse","nouse","nouse", "L_hand_yaw","L_hand_thumb","L_hand_index","L_hand_mid","L_hand_ring","L_hand_pinky", "R_hand_yaw","R_hand_thumb","R_hand_index","R_hand_mid","R_hand_ring","R_hand_pinky"]

#ser.open()


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
			print "move left_shoulder_roll"
			motion_deg = input("take in(0-180)>")
			if motion_deg < 0:
				print "range out"
				motion_deg = 0
			motion_shoulder_roll = 32768 + motion_deg * 97
			print motion_shoulder_roll
			motion_shoulder_roll = '%x' % motion_shoulder_roll
			print motion_shoulder_roll
			#motion = "@00c8:T8000:T8000:T" + motion_shoulder_roll + ":T0000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n"
			#print motion
			ser.write("@00c8:T8000:T8000:T" + motion_shoulder_roll + ":T0000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000:T8000::::::T8000:T8000:T6800:T9800:T6800:T9800:T8000:T8000:T9800:T6800:T9800:T6800\n")
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
		


