# Imports

from Instance import Instance, PlayerGui, workspace
from Common import UDim2
import Render
from pygame.math import Vector2
from pygame import Color
import Enum

# FPS

FPS = Instance.new("Frame", PlayerGui)
FPS.Position = UDim2(0,5,1,-5)
FPS.Size = UDim2(0,100,0,30)
FPS.AnchorPoint = Vector2(0,1)
FPS.BackgroundColor = Color(0,0,0)
FPS.BackgroundTransparency = 0.5

FPSLabel = Instance.new("Label", FPS)
FPSLabel.Size = UDim2(0.9,0,0.75,0)
FPSLabel.Text = "FPS: 0"
FPSLabel.TextScaled = True
FPSLabel.Position = UDim2(0.5,0,0.5,0)
FPSLabel.AnchorPoint = Vector2(0.5,0.5)
FPSLabel.TextColor = Color(0,255,0)
FPSLabel.BackgroundTransparency = 1

def UpdateFPS(dt):
	FPSLabel.Text = "FPS: " + str(round(workspace.FPS * 10) / 10)
	if workspace.FPS < Render.FPSCap/4:
		FPSLabel.TextColor = Color(255,50,50)
	elif workspace.FPS < Render.FPSCap/1.5:
		FPSLabel.TextColor = Color(255,175,20)
	else:
		FPSLabel.TextColor = Color(0,255,0)
		
Render.Stepped.Connect(UpdateFPS)

# Testing

# Label = Instance.new("Label", PlayerGui)
# Label.Position = UDim2(0.5,0,0.5,0)
# Label.AnchorPoint = Vector2(0.5,0.5)
# Label.Text = "Text Here"
# Label.TextWrapped = False
# Label.TextScaled = False
# Label.Size = UDim2(0.4,0,0.5,0)
# Label.TextXAlign = Enum.TextXAlign.Right
# Label.TextYAlign = Enum.TextYAlign.Center