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
from time import sleep

if __name__ == '__main__':
        cmd = str(raw_input('type : \n s/S to scan ports 0-10 \n c/C to configure ports for Potring \n'))
        #print cmd
        #print len(cmd)
        
        if len(cmd) == 1 and ('s' in cmd or 'S' in cmd):
                print "start scanning ports"
                for num in range(11):
                        port = 'COM'+str(num)
                        try:
                                ser = serial.Serial(port, 9600, timeout=0)
                                print (port+"\t OK \n")
                                sleep(0.1)
                                ser.close()
                        except:
                                print (port+"\t -- \n")
                                pass
                raw_input("entree pour quitter")
        if len(cmd) == 1 and ('c' in cmd or 'C' in cmd):
                raw_input("debrancher les 2 cartes arduino svp")
                sleep(0.5)
                p0=''
                p1=''
                raw_input("brancher uniquement l'arduino du capteur de gauche svp")
                sleep(0.5)
                for num in range(11):
                        port = 'COM'+str(num)
                        try:
                                ser0 = serial.Serial(port, 9600, timeout=0)
                                print (port+"\t OK \n")
                                p0=port
                                break
                        except:
                                pass
                raw_input("brancher le deuxieme arduino en plus svp")
                sleep(0.5)
                for num in range(11):
                        port = 'COM'+str(num)
                        try:
                                ser1 = serial.Serial(port, 9600, timeout=0)
                                print (port+"\t OK \n")
                                p1=port
                                break
                        except:
                                pass
                ser0.close()
                ser1.close()
                if p0!='' and p1!='':
                        outline = "p0: "+p0+"\n"+"p1: "+p1
                        print outline
                        with open("ports.config", "w") as file:
                                file.write(outline)
                else:
                        print "erreur"
                raw_input("entree pour quitter")
