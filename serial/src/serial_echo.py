#!/usr/bin/env python
import serial
import time
 
ser=serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    timeout = None,
    xonxoff = 0,
    rtscts = 0,
#    interCharTimeout = None
)
 
#ser.open()
 
while 1:
    print ser.readline(),
