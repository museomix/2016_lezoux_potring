#!/usr/bin/env python
#-*- coding: utf-8 -*-


from libs.arduinoserial import arduinoserial
import glob
from time import sleep

ports = glob.glob('/dev/ttyA*')
arduino = arduinoserial.SerialPort(ports[0], 9600)

while True:
	print arduino.read_until('\n')
		
print "bye"




