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
tags=['4CA684','4CAB53','4CAB3E']
    
##############################
##############################
def chercher_arduino(MAIN):
    try:
        #ser = serial.Serial('COM5', 9600, timeout=1, parity='N')
        with open("ports.config", "r") as file:
            port0 = 'COM'+str(int(file.readline().split('COM', 1)[1]))
            port1 = 'COM'+str(int(file.readline().split('COM', 1)[1]))
            print port0
            print port1
    except:
        print ("\n pas de fichier de config des ports... lancer check_ports.py svp\n")
        j.jeu_go = False
    try:
        ser0 = serial.Serial(port0, 9600, timeout=0)
        ser1 = serial.Serial(port1, 9600, timeout=0)
    except:
        print ("\n probleme avec les cartes arduino. les rebrancher ou relancer check_ports.py\n")
        j.jeu_go = False        

    print ("rfid okay")
    sleep(1)
    while j.jeu_go:
        try:
            line = ser0.readline()
            if line != "": print line
            if ('VOID' in line):
                j.remplir(0,-1)
            elif (tags[0] in line):
                j.remplir(0,0)
            elif (tags[1] in line):
                j.remplir(0,1)
            elif (tags[2] in line):
                j.remplir(0,2)
        except ser0.timeout:
            print('Data could not be read')
        try:
            line = ser1.readline()
            if line != "": print line
            if ('VOID' in line):
                j.remplir(1,-1)
            elif (tags[0] in line):
                j.remplir(1,0)
            elif (tags[1] in line):
                j.remplir(1,1)
            elif (tags[2] in line):
                j.remplir(1,2)
        except ser1.timeout:
            print('Data could not be read')
####################
if __name__ == '__main__':
    j.jeu_go = True
    j.reset_ring()
    chercher(MAIN=True)
    if j.jeu_go==False:
        try:
            ser0.close()
        except:
            pass
        try:
            ser1.close()
        except:
            pass
