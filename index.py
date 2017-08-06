#!/usr/bin/env python3

import pyglet
import pyxhook
import time
import datetime
from threading import Thread
from sys import argv

player = pyglet.media.Player()
file = pyglet.media.load(argv[1], streaming=True)
player.queue(file)

hooking = True

#Pyglet
w = pyglet.window.Window(width = 250, height = 100, caption = argv[1])

def back(n):
	global player
	if player.time - n > 0:
		player.seek(player.time - n)

def player_toggle():
	if player.playing:
		player.pause()
	else:
		back(1)
		player.play()

def get_time():
	global player
	return str(datetime.timedelta(seconds=player.time))[:-4]

@w.event
def on_close():
	global hookman, hooking
	hooking = False
	hookman.cancel()

@w.event
def on_draw():
	global hooking
	w.clear()
	label = pyglet.text.Label('Hello, world', font_name='Times New Roman', font_size=12, x=w.width//2, y=w.height//2, anchor_x='center', anchor_y='center').draw()
	
def update(dt):
	w.set_caption(get_time())

pyglet.clock.schedule_interval(update, 1/7)

#pyxhook
def kbevent(event):
	global hooking, player
	if event.Key == "F2":
		player_toggle()
	if event.Key == "F4":
		back(3)

hookman = pyxhook.HookManager()
hookman.KeyDown = kbevent
hookman.HookKeyboard()

def hook():
	global hooking
	hookman.start()
	while hooking:
		time.sleep(.5)

#Starting Pyglet and pyxhook
hook = Thread(target=hook)
hook.start()
pyglet.app.run()
