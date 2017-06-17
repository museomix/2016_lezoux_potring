#! /usr/bin/python
#-*- coding: utf-8 -*-
####################
# Potring 2.0 <potringpotring@gmail.com>
# voir http://www.museomix.org/prototypes/potring/
# copyright (c) 06/2017 Samuel Braikeh <samuel.braikeh@gmail.com>
# license GNU GPL v.2
####################
# tester les ports série (sur quels ports les arduinos sont branchés)
####################


import serial
if __name__ == '__main__':
        cmd = str(raw_input('type s/S to scan ports 0-10 or a specific port number to test it. '))
        #print cmd
        #print len(cmd)
        if len(cmd) == 1 and ('s' in cmd or 'S' in cmd):
                print "start scanning ports"
                for num in range(11):
                        port = 'COM'+str(num)
                        try:
                                ser = serial.Serial(port, 9600, timeout=0)
                                print (port+"\t OK \n")
                        except:
                                print (port+"\t -- \n")
                                pass

