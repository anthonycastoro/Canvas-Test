from Instance import workspace
import Enum, Render, Input
import pygame as game
from pygame.math import Vector2

def Update(dt):
	cam = workspace.CurrentCamera
	if not cam: return

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

Render.Stepped.Connect(Update)