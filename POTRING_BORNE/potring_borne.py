#!/usr/bin/env python
#-*- coding: utf-8 -*-
####################
# Potring 2.0 <potringpotring@gmail.com>
# voir http://www.museomix.org/prototypes/potring/
# copyright (c) 04/2017 Samuel Braikeh <samuel.braikeh@gmail.com>
# license GNU GPL v.2
####################
# le fichier prncipal
####################

from settings import *
import gtk
import gobject
import threading
#gtk.gdk.threads_init()
import sys
from libs.vlc import vlc
import time
from gettext import gettext as _

from videoclasses import *
from recherche_arduino import *

max_i = 10
gobject.threads_init()

    ####################    ####################    ####################    ####################
class VideoPlayer:
	def __init__(self):
		self.vlc = DecoratedVLCWidget()
		self.vlc.player.set_rate(1)
	def v_init(self,fname):
		self.vlc.player.stop()
		self.vlc.player.set_media(instance.media_new(fname))
	def pause(self):
		self.vlc.player.pause()
	def stop(self):
		self.vlc.player.stop()
	def play(self):
		self.vlc.player.play()
	# second lecteur
	def s_v_init(self,fname):
		self.vlc.s_player.stop()
		self.vlc.s_player.set_media(instance.media_new(fname))
	def s_pause(self):
		self.vlc.s_player.pause()
	def s_stop(self):
		self.vlc.s_player.stop()
	def s_play(self):
		self.vlc.s_player.play()
	def main(self):
		w = gtk.Window()
		w.resize(900,700)
		#w.fullscreen()
		w.add(self.vlc)
		w.show_all()
                w.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#aaaaaa'))
                w.connect("destroy", gtk.main_quit)
		gtk.main()


###################################################"

####################    ####################    ####################    ####################

####################    ####################    ####################    ####################


def maz(): 
  print("mAz")
  global tm_av
  j.reset()
  if j.ring_vide() :
    #print("super... mnt remplis ton ring !")
    p.vlc._label.set("super... mnt remplis ton ring !")
    p.s_v_init("../data3/place_ring.wav")
    p.s_play()
    ##hey, tu dors ?
    #tm_av = gtk.timeout_add(10000,appel_visiteur)
    return (-1,attente_joueurs)
  else:
    print("vide d'abord le ring stp")
    p.vlc._label.set("vide le ring pour recommencer stp")
    p.s_v_init("../data3/vide_le_ring.wav")
    p.s_play()
    return (-1,maz)

def attente_joueurs():
    global tm_lc_2
    global tm_av
    global tm_go
    global tm_ur_go
    print j.ring
    p.vlc.update_progess()
    try:gtk.timeout_remove(tm_go)
    except:pass
    try:gtk.timeout_remove(tm_ur_go)
    except:pass
    try:gtk.timeout_remove(tm_av)
    except:pass
    j.set_change_off()
    if j.ring_rempli() == True :
        #print " ok  cest bientôt le combat, attention ..."
        p.vlc._label.set("bientôt le combat, attention ...")
       # p.v_init("../data2/timer.mp4")
        #p.play()
        p.s_v_init("../data3/compte_a_rebours.wav")
        p.s_play()
        return (0,validation)
    else:
        print("oups.. encore?")
        #tm_av = gtk.timeout_add(10000,appel_visiteur)
        #tm_lc_2 = gtk.timeout_add(max_i*1000*3+20,last_chance_2,False,"es-tu là? remplis le ring..!")
        return (-1,attente_joueurs)

def validation():
        j.set_lecture_on()
        while True:
                if j.change:
                        p.stop()
                        p.s_stop()
                        p.s_v_init("../data3/place_ring_2.wav")
                        p.s_play()
                        j.set_lecture_off()
                        j.set_change_off() # tentative debug
                        return (-1,attente_joueurs)
                elif not j.lecture:
                        #print "c'est Go le combat !"
                        p.vlc._label.set("GO !")
                        j.potiers=list(j.ring)  #le list est super important pour ne pas copier seulement la référence !
                        stats.add_partie(j.potiers)
                        p.vlc._label.set ("pot' " + str(j.ring[0]) + " contre  pot' " + str(j.ring[1]) )
                        return (0,go)
                sleep(0.05)

def go():
	pot_name="P"+str(j.potiers[0])+"P"+str(j.potiers[1])
	if j.numQuestion==0:
		print("lire video 0")
		v_name="../data/"+pot_name+"/"+pot_name+"_q0.mp4"
		print v_name
	else:
		print("num question     = "+str(j.numQuestion))
		print("num ObjetSouleve = "+str(j.numObjetSouleve))
		print("lire video  " + "_q"+str(j.numQuestion)+"_"+str(j.numObjetSouleve) )
		v_name="../data/"+pot_name+"/"+pot_name+"_q"+str(j.numQuestion)+"_"+str(j.numObjetSouleve)+".mp4"
		print v_name
	p.v_init(v_name)
	p.play()
	p.vlc.update_progess()
        j.set_change_off()      #  tentative debug
	return (0,lire_video)

def lire_video():
        p.s_stop()
	j.set_lecture_on()
	sleep(1)
	while True:
		if j.change:
			if j.ring != j.potiers:
				j.reset_erreurs()
				return (0,conflit)
		if not j.lecture: # la vidéo s'est arrêtée
			if(j.numQuestion==2): # fin du jeu ?
				return(0,fin_partie)
			else: # sinon suite, on attend le choix du visiteur
				j.set_numquestion()
				return (0,check_souleve)
		if not j.jeu_go:
			return(0,maz)
		sleep(0.05)

def conflit(): #conflit pendant la lecture d'une vidéo
        j.set_change_off() # tentative debug
	p.pause() # pause; lancer la voix qui dit hey, remets moi ou sinon on quitte
	p.s_v_init("../data3/booh2.wav")
	p.s_play()
	j.set_lecture_on()
	#print ("remets tout comme avant stp.")
	p.vlc._label.set("oh, oh. Remets tes deux poteries en place stp")
	while True:
		if not j.lecture:
			break
		if j.change:
			if j.ring == j.potiers:
				break
		sleep(0.1)
	if j.ring == j.potiers:
		p.s_stop()
		p.play()
		p.vlc.update_progess()
		return(0,lire_video)
	else:
		print ("bon on va recommencer, ok.")
		p.s_stop()
		return (0,abandon)

def check_souleve():
        j.set_lecture_on()   # test debug !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #print("soulève un pot, celui que tu preferes")
        p.vlc._label.set("soulève un pot, celui que tu preferes")
        p.s_v_init("../data3/souleve_pr_voter.wav")
        p.s_play()

        if (j.ring[0]==-1 and j.ring[1]==j.potiers[1])or (j.ring[1]==-1 and j.ring[0]==j.potiers[0]):
                if j.ring[0]==-1 : j.numObjetSouleve=0
                else : j.numObjetSouleve=1
                print("repose-le stp")
                p.vlc._label.set("ok, reposes le !")
                p.s_v_init("../data3/vote_ok.wav")
                p.s_play()
                ##hey, tu dors ?
                return (-1,check_repose)
        elif j.ring==j.potiers:
                return(-1,check_souleve)
        else:
                j.reset_erreurs()
                return(0,conflit2)

        
def check_repose():
	print j.ring
	if j.ring==j.potiers:
		return (0,go)
	else:
		j.reset_erreurs()
		return(0,conflit2)

def conflit2(): #conflit pendant le choix d'un objet
         # pause; lancer la voix qui dit hey, remets moi ou sinon on quitte
        #print ("remets tout comme avant stp.")
        p.pause()
        p.s_v_init("../data3/booh2.wav")
        p.s_play()
        j.set_lecture_on()
        p.vlc._label.set("oh, oh. Remets tes deux poteries en place stp")
        while True:
                if not j.lecture:
                        break
                if j.change:
                        j.set_change_off() # tentative debug
                        if j.ring == j.potiers:
                                break
                sleep(0.05)
        if j.ring == j.potiers:
                p.s_stop()
                #p.play()
                return(0,check_souleve)
        else:
                #print ("bon on va recommencer, ok.")
                p.vlc._label.set("abandon de la partie")
                p.s_stop()
                return(0,abandon)

def abandon():
	#print "tu veux quitter cette partie"
	p.vlc._label.set("abandon de la partie")
	#stats.print_stats()
	#p.v_init("../data2/gameover.mp4")
	#p.play()
	p.s_v_init("../data3/game_over.wav")
	p.s_play()
	j.set_lecture_on()
	while True:
		if not j.lecture:
			break
		sleep(0.05)
	return (0,maz)

def fin_partie():
	# update stats
	print "tu veux quitter cette partie"
	#stats.print_stats()
	#p.v_init("../data2/youppie.mp4")
	#p.play()
	p.s_v_init("../data3/game_over.wav")
	p.s_play()
	j.set_lecture_on()
	while True:
		if not j.lecture:
			break
		sleep(0.05)
	return (0,maz)


def lejeu():
	while j.jeu_go:
		print str(j.etat)
		sss,etat_suivant = j.etat()
		j.set_etat(etat_suivant)
		if sss != -1 :
			sleep(sss)
		else:
			while not j.change:
				sleep(0.05)
			j.set_change_off()


if __name__ == '__main__':
    
    p=VideoPlayer()
    p.vlc.player.set_rate(2)

    j.jeu_go=True
    j.reset_ring()
    print("depart !")    
    
    pulse_cherche = threading.Thread(target=chercher)
    pulse_cherche.start()
    
    j.set_etat(maz)
    pulse_jeu = threading.Thread(target=lejeu)
    pulse_jeu.start()
    
    p.main()
    
    print "bye ..."
    j.jeu_go=False
    
    pulse_cherche.join()
    print "bye cherche"
    pulse_jeu.join()
    print "bye jeu"
    
    print "bref bye."
    
