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

###############
def chercher(MAIN=False):
    chercher_arduino(MAIN)
    #chercher_clavier(MAIN)
###############
    
##############################
##############################
def chercher_arduino(MAIN):
    try:
        #ser = serial.Serial('COM5', 9600, timeout=1, parity='N')
        ser0 = serial.Serial('COM5', 9600, timeout=0)
    except:
        try:
            ser0 = serial.Serial('COM6', 9600, timeout=0)
        except:
            print ("\n erreur.\n essayer de debrancher - rebrancher la carte arduino\n")
            #sys.exit()
            j.jeu_go = False
        

    print ("rfid okay")
    sleep(1)
    while j.jeu_go:
	try:
            line = ser0.readline()
            if line != "": print line
            if ('4D4B7E' in line):
                j.remplir(0,-1)
		j.remplir(1,-1)
		j.remplir(0,0)
		j.remplir(1,1)
	    if ('VOID' in line):
                j.remplir(0,-1)
		j.remplir(1,-1)
            if ('4CA86F' in line):
		j.remplir(0,-1)
		j.remplir(1,-1)
		j.remplir(0,1)
		j.remplir(1,2)
	except ser0.timeout:
            print('Data could not be read')
            sleep(0.1)
####################
if __name__ == '__main__':
    j.jeu_go = True
    chercher(MAIN=True)
