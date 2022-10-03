# Imports

import pygame as game
from Instance import workspace

# Methods

def KeyExists(name):
	return hasattr(game, FixKeyName(name))

def GetKey(name):
	if type(name) == int: return name
	if KeyExists(name): return getattr(game, FixKeyName(name))

def FixKeyName(name):
	if type(name) == int: return name
	
	if hasattr(game, "K_" + name.upper()):
		return "K_" + name.upper()
	elif hasattr(game, "K_" + name.lower()):
		return "K_" + name.lower()
	else:
		return name

def IsKeyDownNow(event, *names):
	if event.type != game.KEYDOWN: return False
	for name in names:
		if event.key == GetKey(name):
			return True
	return False

def IsKeyDown(*names):
	keys = game.key.get_pressed()
	for name in names:
		if GetKey(name) and keys[GetKey(name)]:
			return True
	return False