# Common/Shared Methods

import threading, time, warnings
from random import randint
import pygame as game

def random(min=None, max=None):
	if not min and not max:
		return randint(0, 10000)/10000
	else:
		return randint(min, max)

clamp = lambda n, small, big: max(small, min(n, big))

def spawn(callback, *args, **kwargs):
	threading.Thread(target=callback, args=args, kwargs=kwargs).start()

def delay(callback, t, *args, **kwargs):
	threading.Timer(t, callback, args=args, kwargs=kwargs).start()

def wait(t):
	time.sleep(t)

def warn(msg, type=RuntimeWarning):
	warnings.warn(msg, type)

class UDim: # Contains Scale and Offset for either axis for UI
	Scale = 0
	Offset = 0
	def __init__(self, scale=0, offset=0):
		self.Scale = scale
		self.Offset = offset
		def err():
			raise Exception("Can't set value of UDim")
		self.__setattr__ = err

class UDim2: # Value describing either the position or size of a UI element
	X = None
	Y = None
	def __init__(self, xs=0, xo=0, ys=0, yo=0):
		self.X = UDim(xs, xo)
		self.Y = UDim(ys, yo)
		def err():
			raise Exception("Can't set value of UDim2")
		self.__setattr__ = err
	def fromOffset(xo, yo):
		return UDim2(0,xo,0,yo)
	def fromScale(xs, ys):
		return UDim2(xs,0,ys,0)

def toAlpha(trans):
	return clamp((1 - trans) * 255, 0, 255)

def AspectRatioScale(surface,bx,by):
    ix,iy = surface.get_size()
    if ix > iy: # Width Scale
        factor = bx / float(ix)
        sy = factor * iy
        if sy > by:
            factor = by / float(iy)
            sx = factor * ix
            sy = by
        else:
            sx = bx
    else: # Height Scale
        factor = by / float(iy)
        sx = factor * ix
        if sx > bx:
            factor = bx / float(ix)
            sx = bx
            sy = factor * iy
        else:
            sy = by

    return game.transform.scale(surface, (sx,sy))