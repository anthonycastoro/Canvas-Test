import pygame as game
from pygame.math import Vector2
from Instance import Instance, workspace
from pygame import Color

# Player Handler

Player = Instance.new("Player")
Player.Name = "LocalPlayer"
Player.Parent = workspace
Player._Locked = True

# Character Handler

Character = Instance.new("Rect")
Character.Size = Vector2(5,5)
Character.Position = Vector2(15,10)
Character.Color = Color(220,10,10)
Character.Anchored = False
Character.Name = "Character"
Character.Parent = workspace
Player.Character = Character