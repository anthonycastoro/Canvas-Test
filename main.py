# Imports

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from Instance import Instance, workspace, PlayerGui
from pygame.math import Vector2
from pygame import Color
from Common import *
import Render, Enum

Render.FPSCap = 40

# Border Creation

w = 40
h = 160

Floor = Instance.new("Rect")
Floor.Position = Vector2(h,-w/2)
Floor.Size = Vector2(h*2,w)
Floor.Color = Color(235, 223, 178)
Floor.Unchanging = True
Floor.Name = "Floor"
Floor.Parent = workspace

Left = Floor.Clone()
Left.Position = Vector2(-w/2,h/2)
Left.Size = Vector2(w + 0.5, h+w*2)
Left.Name = "Left"
Left.Parent = workspace

Right = Floor.Clone()
Right.Position = Vector2(h*2+w/2,h/2)
Right.Size = Vector2(w + 0.5, h+w*2)
Right.Name = "Right"
Right.Parent = workspace

Top = Floor.Clone()
Top.Position = Vector2(h,h+w/2)
Top.Size = Vector2(h*2,w)
Top.Name = "Top"
Top.Parent = workspace

# Testing Music

workspace.MasterVolume = 0.7
bg = Instance.new("Sound")
bg.Path = "music/Desperation"
bg.Looped = True
bg.Volume = 1
bg.Pan = 0

delay(lambda: bg.Play(), 2)

Load = Instance.new("Sound")
Load.Path = "sfx/checkpoint/Load" + str(random(1,2))
Load.Volume = 1
Load.Play()

Floor.Changed.Connect(lambda x: print(x, "Changed"))
Top.Changed.Fire()