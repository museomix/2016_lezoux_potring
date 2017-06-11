#!/usr/bin/env python
#-*- coding: utf-8 -*-
####################
# Potring 2.0 <potringpotring@gmail.com>
# voir http://www.museomix.org/prototypes/potring/
# copyright (c) 04/2017 Samuel Braikeh <samuel.braikeh@gmail.com>
# license GNU GPL v.2
####################
# mets j.ring à jour selon l'état des contacteurs/lecteurs rfid
####################

from time import sleep
from collections import deque, defaultdict
from operator import itemgetter
from settings import *

import sys
import msvcrt
import serial
import time

###############
def chercher(MAIN=False):
    chercher_arduino(MAIN)
    #chercher_clavier(MAIN)
###############
try:
    ser0 = serial.Serial('COM5', 9600, timeout=0)
except:
    try:
        ser0 = serial.Serial('COM6', 9600, timeout=0)
    except:
        ser=0
        pass

##############################
##############################
def chercher_arduino(MAIN):
    #ser = serial.Serial('COM5', 9600, timeout=1, parity='N')
    if ser0==0: print "snif"
    print ("wait...")
    time.sleep(1)

    while j.jeu_go:
	try:
            line = ser0.readline()
            if line != "": print line
            if ('010F4D4B7E' in line):
                j.remplir(0,-1)
		j.remplir(1,-1)
		j.remplir(0,0)
		j.remplir(1,1)					
            if ('010F4CA8658F' in line):
		j.remplir(0,-1)
		j.remplir(1,-1)
		j.remplir(0,1)
		j.remplir(1,2)
	except ser0.timeout:
            print('Data could not be read')
            time.sleep(0.1)
####################
if __name__ == '__main__':
    j.jeu_go = True
    chercher(MAIN=True)
