import pygame as game
import os
os.system("clear")

from Instance import Instance, workspace
from pygame.math import Vector2
from pygame import Color
import Render

# Game

Floor = Instance.new("Rect", workspace)
Floor.Position = Vector2(25/2,-5/2)
Floor.Size = Vector2(25, 5)
Floor.Color = Color(235, 223, 178)
Floor.Unchanging = True

Left = Instance.new("Rect", workspace)
Left.Position = Vector2(-5/2,25/2)
Left.Size = Vector2(5.5, 35)
Left.Color = Color(235, 223, 178)
Left.Unchanging = True

# Ceil = Instance.new("Rect", workspace)
# Ceil.Position = Vector2(1000,1550)
# Ceil.Size = Vector2(2500, 300)
# Ceil.Color = Color(235, 223, 178)

# Left = Instance.new("Rect", workspace)
# Left.Position = Vector2(-400,700)
# Left.Size = Vector2(300, 2000)
# Left.Color = Color(235, 223, 178)

# Right = Instance.new("Rect", workspace)
# Right.Position = Vector2(2400,700)
# Right.Size = Vector2(300, 2000)
# Right.Color = Color(235, 223, 178)

bg = Instance.new("Sound")
bg.Path = "music/Cornman.mp3"
bg.Looped = True
bg.Volume = 0.5
bg.Pan = 0
bg.MaxDistance = 5

bg.Play()
print("Played")