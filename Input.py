# Imports

import pygame as game
from Instance import workspace
from Signal import Signal
import Enum

# Methods

def IsKeyDown(*codes):
	for code in codes:
		id = Enum.Reveal(Enum.KeyCode, code).Value
		if game.key.get_pressed()[id]:
			return True
	return False

def IsFocused(): return game.mouse.get_focused()
	
# Events

InputBegan = Signal() # When key is pressed
InputEnded = Signal() # When key is released
InputChanged = Signal() # When mouse moves
InputUnknown = Signal() # When unhandled input is read