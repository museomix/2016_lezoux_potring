#! /usr/bin/python
#-*- coding: utf-8 -*-
##############
#!/usr/bin/env python
#-*- coding: utf-8 -*-
####################
# Potring 2.0 <potringpotring@gmail.com>
# voir http://www.museomix.org/prototypes/potring/
# copyright (c) 04/2017 Samuel Braikeh <samuel.braikeh@gmail.com>
# license GNU GPL v.2
####################
# les classes de video
####################

from settings import *
from libs.vlc import vlc
import gtk
from gettext import gettext as _
import sys

# Create a single vlc.Instance() to be shared by (possible) multiple players.
instance = vlc.Instance()

class VLCWidget(gtk.DrawingArea):
	"""Simple VLC widget."""
	def __init__(self, *p):
		gtk.DrawingArea.__init__(self)
		self.player = instance.media_player_new()
		my_event_manger = self.player.event_manager()
		my_event_manger.event_attach(vlc.EventType.MediaPlayerEndReached, video_end_reached)
		def handle_embed(*args):
			if sys.platform == 'win32':
				self.player.set_hwnd(self.window.handle)
			else:
				self.player.set_xwindow(self.window.xid)
			return True
		self.connect("map", handle_embed)
		self.set_size_request(1000, 1000)
	def set_size(self,w,h):
		self.set_size_request(w, h)

	####################    ####################    ####################    ####################

def video_end_reached(self):
	print("fin de la video")
	j.set_lecture_off()
	print(" ou ... fin du son")
	
####################    ####################    ####################    ####################

class DecoratedVLCWidget(gtk.VBox):
    """Decorated VLC widget."""
    def __init__(self, *p):
        gtk.VBox.__init__(self)
        self._vlc_widget = VLCWidget(*p)
        self.player = self._vlc_widget.player
        self.pack_start(self._vlc_widget, expand=True)
        self._widget_son = VLCWidget(*p)
        self._widget_son.set_size(0,0)
        self.s_player = self._widget_son.player
        self.pack_start(self._widget_son, expand=True)
        # self.tetes = gtk.HBox(True, 3)
        self._im0 = gtk.Image()
        self._im1 = gtk.Image()
        # self.tetes.add(self._im0)
        # self.tetes.add(self._im1)
        # self.pack_start(self.tetes, expand=False)
        self._label = gtk.Label("mini pot contre gros pot")
        self.pack_start(self._label, expand=False)

    def update_progess(self):
        self._label.set_text("P"+str(j.ring[0])+" versus P"+str(j.ring[1]))
        return False


