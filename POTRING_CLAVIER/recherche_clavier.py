#!/usr/bin/env python
#-*- coding: utf-8 -*-
####################
# Potring 2.0 <potringpotring@gmail.com>
# voir http://www.museomix.org/prototypes/potring/
# copyright (c) 04/2017 Samuel Braikeh <samuel.braikeh@gmail.com>
# license GNU GPL v.2
####################
# mets j.ring à jour selon l'état des contacteurs
####################

from time import sleep
from settings import *
import serial
import sys
import settings

###############

def chercher(MAIN=False):
   #chercher_arduino(MAIN)
    chercher_clavier(MAIN)

##############################

def chercher_clavier(MAIN):
	while j.jeu_go:
		oo=sys.stdin.read(1)
		if oo=="a":
			if j.ring[0]==-1:j.remplir(0,0)
			elif j.ring[0]==0:j.remplir(0,-1)
		elif oo=="z":
			if j.ring[0]==-1:j.remplir(0,1)
			elif j.ring[0]==1:j.remplir(0,-1)
		elif oo=="e":
			if j.ring[0]==-1:j.remplir(0,2)
			elif j.ring[0]==2:j.remplir(0,-1)
		elif oo=="i":
			if j.ring[1]==-1:j.remplir(1,0)
			elif j.ring[1]==0:j.remplir(1,-1)
		elif oo=="o":
			if j.ring[1]==-1:j.remplir(1,1)
			elif j.ring[1]==1:j.remplir(1,-1)
		elif oo=="p":
			if j.ring[1]==-1:j.remplir(1,2)
			elif j.ring[1]==2:j.remplir(1,-1)
		if MAIN :
			print " potier0 : "+str(j.ring[0])+"        potier1 : "+str(j.ring[1])
			if oo=="q":break
			#if cv2.waitKey(1) & 0xFF == ord('q'):
				#break
####################
if __name__ == '__main__':
	j.jeu_go = True
	j.reset_ring()
	chercher(MAIN=True)
