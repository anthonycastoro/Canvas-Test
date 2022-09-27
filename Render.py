import pygame as game
import sys as system
import threading
import Input

from pygame import Color
from pygame.math import Vector2

import Instance
from Instance import workspace

# game.mixer.pre_init(frequency=44100, size=-16, channels=100)
game.init()
game.event.set_allowed([game.QUIT, game.KEYDOWN, game.KEYUP])

screendata = game.display.Info()
window = game.display.set_mode(
	(screendata.current_w, screendata.current_h), 
	game.FULLSCREEN | game.DOUBLEBUF,
	12
)

game.display.set_caption(" Loading...")
game.display.set_icon(game.image.load("./icon.png").convert_alpha())

# Debug

def DebugDot(pos):
	game.draw.rect(window, Color(0,255,0), game.Rect(pos.x - 2, pos.y - 2, 4, 4))

# Render

running = False
clock = game.time.Clock()
frame = 0	
Delta = 0
clamp = lambda n, small, big:  max(small, min(n, big))
FPSCap = 40

def init():
	global running
	global frame
	global clock
	global Delta
	global clamp
	global FPSCap
	
	if running: return
	
	running = True
	cam = workspace.Camera
	
	while 1:
		frame += 1
		dt = clock.tick(FPSCap) / 1000
		Delta = dt
		
		# Event Handlers

		for event in game.event.get():
			if event.type == game.QUIT:
				game.quit()
				system.exit()
				running = False
				break
		
		if Input.IsKeyDown("w", "up"):
			cam.Position += Vector2(0, dt * cam.Speed.x)
		if Input.IsKeyDown("s", "down"):
			cam.Position -= Vector2(0, dt * cam.Speed.x)
		if Input.IsKeyDown("a", "left"):
			cam.Position -= Vector2(dt * cam.Speed.y, 0)
		if Input.IsKeyDown("d", "right"):
			cam.Position += Vector2(dt * cam.Speed.y, 0)					
		if Input.IsKeyDown("equals", "i"):
			cam.Zoom += dt * cam.ZoomIncrement
			if cam.Zoom > cam.ZoomRange.y:
				cam.Zoom = cam.ZoomRange.y
		if Input.IsKeyDown("minus", "o"):
			cam.Zoom -= dt * cam.ZoomIncrement
			if cam.Zoom < cam.ZoomRange.x:
				cam.Zoom = cam.ZoomRange.x
		
		# Rendering

		if frame % 10 == 0 or frame == 1: game.display.set_caption(" " + workspace.Name)
		if frame % FPSCap == 0: print(workspace.FPS)

		window.fill(workspace.SkyColor)
		for i in Instance.Orientation._Memory:
			if hasattr(i, "Update"): i.Update(dt, window)
			if hasattr(i, "Render") and i.Transparency < 1:	
				if i.IsDescendantOf(workspace):
					# Make Surface
	
					size = i.Size * cam.Zoom
					pos = i.Position * cam.Zoom

					surface = None

					unchanging = i.Unchanging
					if unchanging and i._Surface:
						surface = i._Surface
					else:
						surface = game.Surface((size.x, size.y), game.SRCALPHA).convert_alpha()
						surface.fill(Color(0,0,0,0))
						if unchanging:
							surface.convert()
						unchanging = False

					# Positional Variables
					
					ws = window.get_size()
					cp = cam.Position * cam.Zoom

					i.AbsoluteCenter = Vector2(
						pos.x + ws[0]/2 - cp.x,
						-pos.y + ws[1]/2 + cp.y
					)

					i.AbsoluteCorner = Vector2(
						pos.x + ws[0]/2 - cp.x - size[0]/2,
						-pos.y + ws[1]/2 + cp.y - size[1]/2
					)

					dontblit = False
					if unchanging: # Scale without recreating surface
						p = i.AbsoluteCorner
						s = size
						op = p
						p = Vector2(clamp(p.x,0,ws[0]), clamp(p.y,0,ws[1]))
						s = Vector2(
							s.x-p.x,
							s.y-p.y
						) + op
						s = Vector2(
							clamp(s.x+p.x,0,ws[0]),
							clamp(s.y+p.y,0,ws[1])
						) - p
						
						i.AbsoluteCorner = p
						if s.x > 0 and s.y > 0 and p.x < ws[0] and p.y < ws[1]:
							surface = game.transform.scale(surface, (s.x, s.y))
							dontblit = False
						else: 
							surface = game.transform.scale(surface, (1,1))
							dontblit = True
						
					i._Surface = surface

					# Adjust Surface
					
					if i.Transparency > 0: surface.set_alpha((1 - i.Transparency) * 255)
					
					# Render to surface and rotate
					i.Render(surface, dt)
					if i.Rotation != 0 and not unchanging: surface = game.transform.rotate(surface, i.Rotation)
	
					# Paint to Window

					if not dontblit:
						window.blit(surface, (
							i.AbsoluteCorner.x,
							i.AbsoluteCorner.y
						))
										
					i._Changed = False
		
		# Finalize

		workspace.FPS = clock.get_fps()
		game.display.update()

threading.Thread(target=init).start()