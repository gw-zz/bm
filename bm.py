#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bm.py - BM - Quick and dirty bm widget 
#
# NO Copyright - by gw 
# Released under a What the fuck you want license
#
# Changelog
# 15/12/08 - 0.1 - Initial release

"""
Classes : 
	Bm_image : Gtk interface
Constants:
	IMAGEDIR : Image cache directory
""" 

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import feedparser
import urllib
from HTMLParser import HTMLParser

__version__ = '0.1'
__author__ = 'gw'

IMAGEDIR=os.path.join(os.path.dirname(__file__), 'img')

class Bm_image:
	""" Bm_image()
	
	Initialize Gtk GUI
	"""

	def __init__(self, fh):
		"""Build gtk interface and connect event to callbacks"""

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("BM widget")	
        	self.window.set_default_size(480, 540)
		self.window.connect('destroy',lambda *w: gtk.main_quit())
		main_vbox = gtk.VBox()
		self.window.add(main_vbox)
		frame_vert = gtk.Frame("BM")
		main_vbox.pack_start(frame_vert,padding=0)
		self.im = gtk.Image()
		pix = gtk.gdk.pixbuf_new_from_file("tumb.jpg")
		#pix = gtk.gdk.pixbuf_new_from_file("test.jpg")
		scal = pix.scale_simple(480,480,gtk.gdk.INTERP_BILINEAR)
		self.im.set_from_pixbuf(scal)
		#im.connect("clicked", self.do_run, self.window)
		self.window.connect("button_press_event", self.do_menu)
		self.window.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		hbox = gtk.HBox()
		hbox.set_border_width(3)
		#hbox.add(gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 400, 600))
		#hbox.add(gtk.Label("No thumb"))
		hbox.add(self.im)
		frame_vert.add(hbox)

		bbox = gtk.HButtonBox()
		frame_bb = gtk.Frame()
		bbox.set_layout(gtk.BUTTONBOX_EDGE)
		bbox.set_spacing(0)
		frame_bb.add(bbox)
		button = gtk.Button("prev")
		button.connect("clicked", self.do_show_prev)
		bbox.add(button)
		button = gtk.Button("next")
		button.connect("clicked", self.do_show_next)
		bbox.add(button)	
		
		main_vbox.pack_start(frame_bb,expand=False)
		self.window.show_all()
		self.handler = fh
	
	def do_show_prev(self,cb):
		print "Show prev"
		pix = gtk.gdk.pixbuf_new_from_file("test.jpg")
		scal = pix.scale_simple(480,480,gtk.gdk.INTERP_BILINEAR)
		self.im.set_from_pixbuf(scal)

	def do_show_next(self,cb):
		print "Show next"
		pix = gtk.gdk.pixbuf_new_from_file("tumb.jpg")
		scal = pix.scale_simple(480,480,gtk.gdk.INTERP_BILINEAR)
		self.im.set_from_pixbuf(scal)


	def do_update(self, cb):
		"""Update current feed"""
		print "Cb : update"	
		self.handler.fetch_feed()

	def do_pref(self, cb):
		"""Launch preferences dialog window"""
		print "Cb : pref"	

	def add_feed(self, cb):
		"""Add a new feed"""
		print "Cb : feed"	

	def quit(self, cb):
		"""Stop gracefuly the application"""
		print "Quit app"
		gtk.main_quit()

	def do_menu(self, widg , event):
		"""Show a popup menu"""

		print "Clicked :", event.button
		popupMenu = gtk.Menu()
		menupop0 = gtk.MenuItem("Update")
		menupop0.connect("activate", self.do_update)
		popupMenu.add(menupop0)
		#menupop1 = gtk.MenuItem("Add New Feed")
		#menupop1.connect("activate", self.add_feed)
		#popupMenu.add(menupop1)
		menupop2 = gtk.MenuItem("Preferences")
		menupop2.connect("activate", self.do_pref)
		popupMenu.add(menupop2)	
		menupop3 = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		menupop3.connect("activate", self.quit)
		popupMenu.add(menupop3)
		popupMenu.show_all()
		popupMenu.popup(None,None, None, 1, 0)

class BMHtmlParser(HTMLParser):
	def __init__(self, feed=None):
		HTMLParser.__init__(self)
		self._img = []

	def handle_starttag(self, tag, attrs):
        	print "Encountered the beginning of a %s tag" % tag
		if tag == "img":
			for name, value in attrs:
				if name == 'src':
					print "Img: ", value
					self._img.append(value)

	def handle_endtag(self, tag):
		print "Encountered the end of a %s tag" % tag

	def get_img(self):
		return self._img

class Feed_handler:
	"""Handle operations on a feed (fetch, update, parse, cache)"""

	def __init__(self, url):
		self.feed_url = url
	
	def fetch_feed(self):
		print "fetch_feed\n"
		parser = feedparser.parse(self.feed_url)
		print parser['feed']['title']
		print parser.keys()
		print "Entries:", len(parser.entries)
		latest = parser.entries[0]
		print latest.keys()
		print "Id", latest.id
		print "title", latest.title
		print "Summary", latest.summary
		print "Summaryd", latest.summary_detail
		bmparser = BMHtmlParser()
		bmparser.feed(latest.summary)
		print bmparser.get_img()
		filename,headers = urllib.urlretrieve(bmparser.get_img()[0], "test.jpg") 
		print "file:", file, " headers", headers
		return True
	
	def update_feed(self):
		pass	


def main():
	gtk.main()
	return 0

if __name__ == "__main__":
	if '-h' in sys.argv[1:] or '--help' in sys.argv[1:]:
		print "Usage: bm url"
		sys.exit(0)
	#url = sys.argv[1:]
	#if len(url) == 0:
	#	print '[Error] : provide at least one url\n'
	#	sys.exit(1)
	default_url = "http://bonjourmadame.fr/rss"
	handler = Feed_handler(default_url)
	Bm_image(handler)
	main()

# End of bm.py
