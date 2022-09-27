import pygame as game
import os
os.system("clear")

from Instance import Instance, workspace
from pygame.math import Vector2
from pygame import Color
import Render

Render.FPSCap = 50
# Game

w = 20
h = 100

Floor = Instance.new("Rect", workspace)
Floor.Position = Vector2(h,-w/2)
Floor.Size = Vector2(h*2,w)
Floor.Color = Color(235, 223, 178)
Floor.Unchanging = True

Left = Instance.new("Rect", workspace)
Left.Position = Vector2(-w/2,h/2)
Left.Size = Vector2(w + 0.5, h+w*2)
Left.Color = Color(235, 223, 178)
Left.Unchanging = True

Right = Instance.new("Rect", workspace)
Right.Position = Vector2(h*2+w/2,h/2)
Right.Size = Vector2(w + 0.5, h+w*2)
Right.Color = Color(235, 223, 178)
Right.Unchanging = True

Ceil = Instance.new("Rect", workspace)
Ceil.Position = Vector2(h,h+w/2)
Ceil.Size = Vector2(h*2,w)
Ceil.Color = Color(235, 223, 178)
Ceil.Unchanging = True

bg = Instance.new("Sound")
bg.Path = "music/FifthOfBeethoven"
bg.Looped = True
bg.Volume = 0.5
bg.Pan = 0
bg.MaxDistance = 5

bg.Play()

print(bg.Clone())