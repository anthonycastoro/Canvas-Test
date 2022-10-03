import pygame as game
import sys as system
import Input
from Common import *

from pygame import Color
from pygame.math import Vector2
from Signal import Signal

import Instance
workspace = Instance.workspace
PlayerGui = Instance.PlayerGui

# game.mixer.pre_init(frequency=44100, size=-16, channels=100)
game.init()
game.mixer.set_num_channels(30)
game.event.set_allowed([game.QUIT, game.KEYDOWN, game.KEYUP])

screendata = game.display.Info()
window = game.display.set_mode(
	(screendata.current_w, screendata.current_h), 
	game.FULLSCREEN | game.DOUBLEBUF,
	12
)

game.display.set_caption(" Loading...")
game.display.set_icon(game.image.load("Image/icon.png").convert_alpha())

# Debug

def DebugDot(pos):
	game.draw.rect(window, Color(0,255,0), game.Rect(pos.x - 2, pos.y - 2, 4, 4))

# Render

running = False
clock = game.time.Clock()
Frame = 0	
Delta = 0
FPSCap = 30
Stepped = Signal()

def init():
	global running, Frame, clock
	global Delta, clamp, FPSCap
	global Stepped
	
	if running: return
	
	running = True
	cam = workspace.Camera
	
	while 1:
		Frame += 1
		dt = clock.tick(FPSCap) / 1000
		Delta = dt
		Stepped.Fire(dt)
		
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
		
		if Frame % 10 == 0 or Frame == 1: game.display.set_caption(" " + workspace.Name)
		#if Frame % FPSCap == 0 or workspace.FPS < 20: print(round(workspace.FPS * 10)/10)
		
		window.fill(workspace.SkyColor)
		for obj in Instance.Orientation._Memory:
			if hasattr(obj, "Update"): obj.Update(dt, window)
		
		for i in workspace.GetChildren():
			if hasattr(i, "Render") and i.IsA("PVObject") and i.Transparency < 1:	
				# Make Surface

				size = i.Size * cam.Zoom
				pos = i.Position * cam.Zoom

				surface = None

				unchanging = i.Unchanging

				if not i._Surface:
					surface = game.Surface((size.x, size.y), game.SRCALPHA).convert_alpha()
					unchanging = False
				else:
					surface = i._Surface

				if not unchanging:
					surface = game.transform.scale(surface, (size.x,size.y))
					surface.fill(Color(0,0,0,0))

				# Positional Variables
				
				ws = window.get_size()
				cp = cam.Position * cam.Zoom

				i.AbsoluteCenter = Vector2(
					pos.x + ws[0]/2 - cp.x,
					-pos.y + ws[1]/2 + cp.y
				)
				i.AbsoluteSize = Vector2(size[0], size[1])
				i.AbsoluteCorner = i.AbsoluteCenter - i.AbsoluteSize / 2
				
				dontblit = False
				if unchanging: # Clamp position and size to inside of window
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
				else: # Don't render if not onscreen
					s = size
					p = i.AbsoluteCorner
					total = s + p
					if total.x < 0 or total.y < 0 or p.x > ws[0] or p.y > ws[1]:
						dontblit = True
					else:
						dontblit = False
								
				# Adjust Surface
				
				if i.Transparency > 0: surface.set_alpha(toAlpha(self.Transparency))
				
				# Render to surface and rotate
				i.Render(surface, dt)
				if i.Rotation != 0 and not unchanging: surface = game.transform.rotate(surface, i.Rotation)

				# Paint to Window

				if not dontblit:
					window.blit(surface, (
						i.AbsoluteCorner.x,
						i.AbsoluteCorner.y
					))

				i._Surface = surface
				i._Changed = False

		for ui in PlayerGui.GetChildren():
			def RenderFrame(ui, topsurface):
				if hasattr(ui, "Render") and ui.IsA("GuiObject"):
					ws = topsurface.get_size()
	
					surface = None
					if not ui._Surface:
						surface = game.Surface((0,0), game.SRCALPHA).convert_alpha()
					else: surface = ui._Surface
					
					sx = ui.Size.X
					sy = ui.Size.Y
	
					xsize = sx.Scale * ws[0] + sx.Offset
					ysize = sy.Scale * ws[1] + sy.Offset
	
					px, py = ui.Position.X, ui.Position.Y
	
					anchor = ui.AnchorPoint
					xpos = (px.Scale * ws[0]) + px.Offset - (anchor.x * xsize)
					ypos = (py.Scale * ws[1]) + py.Offset - (anchor.y * ysize)
					
					ui.AbsoluteSize = Vector2(xsize, ysize)
					ui.AbsoluteCorner = Vector2(xpos, ypos)
					ui.AbsoluteCenter = ui.AbsoluteCorner + ui.AbsoluteSize / 2
					
					surface = game.transform.scale(surface, (xsize, ysize))
					surface = game.transform.rotate(surface, ui.Rotation)	
					
					ui.Render(surface, dt)
					ui._Surface = surface
					ui._Changed = False

					for child in ui.GetChildren():
						RenderFrame(child, surface)
										
					topsurface.blit(surface, (xpos, ypos))

			RenderFrame(ui, window)

		# Finalize

		workspace.FPS = clock.get_fps()
		game.display.update()

spawn(init)