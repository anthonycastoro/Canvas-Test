# Imports

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from Instance import Instance, workspace, PlayerGui
from pygame.math import Vector2
from pygame import Color
from Common import *
import Render, Debug

Render.FPSCap = 50

# Border Creation

w = 20
h = 100

Floor = Instance.new("Rect")
Floor.Position = Vector2(h,-w/2)
Floor.Size = Vector2(h*2,w)
Floor.Color = Color(235, 223, 178)
Floor.Unchanging = True
Floor.Parent = workspace

Left = Floor.Clone()
Left.Position = Vector2(-w/2,h/2)
Left.Size = Vector2(w + 0.5, h+w*2)
Left.Parent = workspace

Right = Floor.Clone()
Right.Position = Vector2(h*2+w/2,h/2)
Right.Size = Vector2(w + 0.5, h+w*2)
Right.Parent = workspace

Ceil = Floor.Clone()
Ceil.Position = Vector2(h,h+w/2)
Ceil.Size = Vector2(h*2,w)
Ceil.Parent = workspace

# Testing Music

bg = Instance.new("Sound")
bg.Path = "music/FifthOfBeethoven"
bg.Looped = True
bg.Volume = 0.5
bg.Pan = 0
bg.MaxDistance = 5

bg.Play(2)

Load = Instance.new("Sound")
Load.Path = "sfx/checkpoint/Load" + str(random(1,2))
Load.Play()