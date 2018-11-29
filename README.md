# SOBIT_blue
Ros package of SOBIT (Robovie R2)

#　author 
Masaaki Yokomizo(soka univ 45th)
...


# Robovie-Maker
ソビットのOC用モーションを作成する
1. roslaunch sobit_description display.launch
		→launch rviz and joint_state_publisher

2. ./sobit_description/src/Robovie_maker.py
		→joint_state_publisher send motion for sobit

3. ./sobit_descrooption/src/save_motion
		→save pose of sobit now amd set motion_time for motion

# sobit_controller
publishされたmotion_degをシリアル通信に変換し、送信する
1. ./sobit_description/sobit_controller

# send_motion
Robovie_makerで作成したモーションファイルの内容をmotion_deg型でpublishする(テスト用）
1. ./sobit_description/send_motion　








