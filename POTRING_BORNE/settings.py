#! /usr/bin/python
#-*- coding: utf-8 -*-
####################
# Potring 2.0 <potringpotring@gmail.com>
# voir http://www.museomix.org/prototypes/potring/
# copyright (c) 04/2017 Samuel Braikeh <samuel.braikeh@gmail.com>
# license GNU GPL v.2
####################
# la classe du jeu avec les variables globales necessaires ; les statistiques aussi
####################


from threading import RLock
verrou = RLock()
##############
class Jeu:
	def __init__(self):
		self.nbObjets = 3
		self.nbKeys = 6
		self.keys = [0]*self.nbKeys
		self.jeu_go=False
		self.reset()
	def reset_ring(self):
		self.ring = [-1,-1]
		self.potiers = [-9,-9]
	def reset(self):
		self.numQuestion=0
		self.etat="maz"
		self.etat2="0"
		self.lecture=False
		self.change=False
		self.souleve=False
		self.numObjetSouleve = -1
		self.erreurs = 0
##############
	def set_etat(self,tata):
		self.etat=tata
##############
	def reset_erreurs(self):
		self.erreurs=0
	def add_erreurs(self):
		self.erreurs+=1
##############
	def set_change_off(self):
		with verrou:
			self.change=False
	def set_lecture_on(self):
		with verrou:
			self.lecture=True
	def set_lecture_off(self):
		with verrou:
			self.lecture=False
	def set_numquestion(self):
		self.numQuestion +=1
##############
	def remplir(self,pos,val):
		with verrou:
                        if self.ring[pos]!=val: # securite supplementaire
                                self.ring[pos]=val
                                #if val == -1: print "je vide"
                                #else: print "je remplis"
				self.change=True
##############
	def ring_rempli(self):
		if self.ring[0] != -1 and self.ring[1] != -1 : return True
		else : return False
	def ring_vide(self):
		if self.ring == [-1,-1] : return True
		else : return False
###############

j=Jeu()

###############
class Stats:
	def __init__(self):
		self.parties = {'p0p1':0, 'p0p2':0, 'p1p2':0}
		self.total=0
		self.gagnants = [[0, 0, 0], \
						 [0, 0, 0], \
						 [0, 0, 0]]
		self.gagnes_totales = 0
		self.parties_finies = 0
	def add_partie(self,potiers):
		if potiers[0]==0 or potiers[1]==0:
			if potiers[0]==1 or potiers[1]==1:
				self.parties['p0p1']+=1
			else:
				self.parties['p0p2']+=1
		else:
			self.parties['p1p2']+=1
		self.total=self.parties['p0p1']+self.parties['p0p2']+self.parties['p1p2']
	def add_gangant(self,potiers,n_gagnant):
		self.gagnes_totales=[self.gagnants[0,1]+self.gagnants[0,2],\
							self.gagnants[1,0]+self.gagnants[1,2],\
							self.gagnants[2,0]+self.gagnants[2,0]]
		self.parties_finies=self.gagnes_totales[0]+self.gagnes_totales[1]+self.gagnes_totales[2]
	def read_stats(self,fname):
		return False
	def print_stats(self):
		print self.parties
		return False
	def write_stats(self,fname):
		return False
###############
stats=Stats()





