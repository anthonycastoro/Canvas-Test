import pygame as game
import os

from pygame import Color
from pygame.math import Vector2
from Common import *

# Instance Orientation

class Orientation:
	_Memory = []
	_DebugId = 0

	# Base Class For Everything
	class Instance:
		_Creatiable = False
		_Service = False
		_ServiceCreated = False
		_Parent = None
		_Children = None
		_Changed = False
		_DebugId = -1
		
		Name = "Instance"
		ClassName = "Unknown"
		Destroyed = False
		
		__str__ = lambda self: self.Name

		def __init__(self):
			self._DebugId = Orientation._DebugId
			Orientation._DebugId += 1
			self._ServiceCreated = None
			self._Creatiable = None
			self._Children = []
		
		def __getattr__(self, name):
			if name == "Parent": return self._Parent
			if name == "HasChanged": return self._Changed
			raise AttributeError(self.ClassName + " does not have the attribute '" + name + "''")
		
		def __setattr__(self, name, value):
			if not isinstance(self, object):
				raise AttributeError("Cannot set index of base class.")

			if getattr(self, name) != value:
				self.__dict__["_Changed"] = True
			
			if name == "Parent":
				if not (isinstance(value, Orientation.Instance) or value == None):
					raise AttributeError("Must set Parent to an Instance or None.")
				before = self._Parent
				self._Parent = value
				if before: before._Children.remove(self)
				if value: value._Children.append(self)
			else:
				self.__dict__[name] = value

		def Destroy(self):
			if not self.Destroyed:
				Orientation._Memory.remove(self)
				self.Parent = None
				self.Destoryed = True
				for child in self._Children:
					child.Destroy()
				self._Children = []
		def Dispose(self):
			self.Destroy()
		def Remove(self):
			self.Destroy()
		
		def IsA(self, ClassName):
			if hasattr(Orientation, ClassName):
				return isinstance(self, getattr(Orientation, ClassName))
			else:
				warn(f"{self.ClassName} is not a '{ClassName}' because it isn't a valid class or abstract class.")
				return False

		def GetChildren(self):
			return self._Children
		def GetDescendants(self):
			descendants = []
			for child in self._Children:
				descendants.append(child)
				descendants.extend(child.GetDescendants())
			return descendants
		
		def FindFirstChild(self, name):
			for child in self._Children:
				if child.Name == name:
					return child
		
		def FindFirstAncestor(self, name):
			parent = None
			while 1:
				parent = self.Parent
				if parent:
					if parent.Name == name:
						return parent
					else:
						parent = parent.Parent
				else:
					return

		def GetDebugId(self):
			return self._DebugId
			
		def IsDescendantOf(self, ancestor):
			parent = None
			while 1:
				parent = self.Parent
				if parent:
					if parent == ancestor:
						return True
					else:
						parent = parent.Parent
				else:
					return
			
		def IsAncestorOf(self, other):
			return other.IsDecendantOf(self)

		def Clone(self):
			if not self._Service:
				cloned = Instance.new(self.ClassName)
				for i, v in vars(self).items():
					if i == "Destroyed": continue
					if i.startswith("_"): continue
					if callable(v): continue
					setattr(cloned,i,v)
				return cloned
			else:
				raise Exception(f"Cannot clone Service '{self.ClassName}'")

	# Services
	class Workspace (Instance):
		_Creatiable = False
		_Service = True
		Name = "Workspace"
		
		SkyColor = Color(125,125,255)
		Gravity = 100
		FPS = 0

		class Camera:
			Position = Vector2(0,0)
			Roll = 0
			Zoom = 50
			ZoomIncrement = 70
			ZoomRange = Vector2(3, 150)
			Speed = Vector2(7,7)

	class PlayerGui (Instance):
		_Creatiable = False
		_Service = True
		Name = "PlayerGui"

		Debug = True
	
	# Abstract Instances
	class PVObject (Instance):
		_Creatiable = False
		
		_Surface = None
		
		Unchanging = False
		Color = Color(200,200,200)
		Velocity = Vector2()
		Position = Vector2()
		Size = Vector2(100,100)
		Rotation = 0
		Transparency = 0
		ZIndex = 1
		
		AbsoluteCorner = Vector2()
		AbsoluteSize = Vector2(100,100)
		AbsoluteCenter = Vector2(50,50)

	# Invisible Instances
	
	class Sound (Instance):
		_Creatiable = True
		_IsPlaying = False
		_Path = ""
		Path = ""
		
		Mixer = None
		Channel = None
		Playing = False
		Paused = False
		Looped = False
		Volume = 1
		Pan = 0

		Length = 0
		
		MaxDistance = 20
		MinDistance = 0
		
		def __init__(self):
			super().__init__()
			self.Channel = game.mixer.Channel(self.GetDebugId())
		
		def __setattr__(self, name, value):
			if name == "Path":
				if self.Mixer: self.Mixer.stop()
				split = value.split("/")
				name = split[-1]
				del split[-1]
				fold = "/".join(split)
				ext = ""
				
				for file in os.listdir("Audio/" + fold):
					if file.startswith(name):
						ext = "." + file.split(".")[-1]
						break
				
				p = "Audio/" + value + ext
				self.Mixer = game.mixer.Sound(p)
				self.Length = self.Mixer.get_length()
				self.__dict__["Path"] = p
			else:
				super().__setattr__(name, value)
		
		def Play(self, wait=0):
			self.Playing = True
			if self.Mixer: 
				if wait != 0:
					delay(lambda: self.Channel.play(self.Mixer), wait)
				else: self.Channel.play(self.Mixer)
				self._IsPlaying = True
		
		def Stop(self):
			if self._IsPlaying:
				self.Playing = False
				if self.Mixer:
					self.Channel.stop()
					self._IsPlaying = False
		
		# Update
		
		def Update(self, dt, window):
			if self.Mixer and self.Channel:
				# Playing Check

				if not self.Playing and self._IsPlaying:
					self.Stop()
				
				# Paused Check
				
				if self.Paused:
					self.Channel.pause()
				else:
					self.Channel.unpause()

				# Volume and Pan Check

				def SetPan(pan, multi=1):
					pan = (pan + 1) / 2 # 0 to 1 instead of -1 to 1
					if pan < 0: pan = 0
					if pan > 1: pan = 1
					self.Channel.set_volume((1 - pan) * multi, pan * multi)
					
				if self.Playing:
					#self.Mixer.set_volume(self.Volume)
					if not self.Parent:
						SetPan(self.Pan)
					else:
						p = self.Parent.AbsoluteCenter.x / window.get_width()
						if p < 0: p = 0
						if p > 1: p = 1
						p = (p - 0.5) * 2
						dist = (self.Parent.Position - workspace.Camera.Position).magnitude()
						max = self.MaxDistance
						min = self.MinDistance
						multi = 1
						if dist > max: 
							multi = 0
							p = 0
						elif dist < min:
							multi = 1
						else:
							multi = (dist - max) / (min - max)
						SetPan(p, multi)

				# Loop Check
				
				if not self.Channel.get_busy():
					if self.Looped and self.Playing:
						self.Play()
					else:
						self.Stop()
		
		def __str__(self):
			p = self.Path
			name = p.split("/")[-1]
			if p.startswith("Audio/sfx"):
				return f"Sound '{name}'"
			elif p.startswith("Audio/music"):
				return f"Soundtrack '{name}'"
			else:
				return super().__str__()

	class GuiObject (Instance):
		_Creatiable = False

		Visible = True
		BackgroundColor = Color(255,255,255)
		BackgroundTransparency = 0
		Size = UDim2.fromOffset(100,100)
		Position = UDim2()
		AnchorPoint = Vector2()
		Rotation = 0
		ZIndex = 1

		AbsoluteCorner = Vector2()
		AbsoluteSize = Vector2(100,100)
		AbsoluteCenter = Vector2(50,50)
		AbsoluteRotation = 0

		_Surface = None

		def Render(self, surface, dt):
			c = self.BackgroundColor
			opacity = int((1 - self.BackgroundTransparency) * 255)
			surface.fill(Color(c.r, c.g, c.b, opacity))
	
	# Visible Workspace Instances
	
	class Rect (PVObject):
		_Creatiable = True
		
		def Render(self, surface, dt):
			surface.fill(self.Color)

	class Frame (GuiObject):
		_Creatiable = True

	class Label (GuiObject):
		_Creatiable = True
		_Face = None
		
		Text = "Label Text"
		Font = "Arial"
		TextTransparency = 0
		TextSize = 14
		TextScaled = True
		TextBounds = Vector2()
		TextWrapped = True
		

# Instance Creator
class Instance:
	services = {}
	def new(className, parent=None, service=False):
		if not hasattr(Orientation, className):
			raise NotImplementedError(f"'{className}' is not a valid class!")
		
		Creator = getattr(Orientation, className)
		Object = None
		
		if service and not Creator._Service:
			raise NotImplementedError(f"'{className}' is not a service!")
		elif Creator._Service and not service:
			raise Exception("Cannot create a service instance normally!")
		elif service and Creator._ServiceCreated:
			return Instance.services[className]
		elif Creator._Service and service:
			Creator._ServiceCreated = True
		
		if Creator._Creatiable or (service and Creator._Service):
			Object = Creator()
			if service: Instance.services[className] = Object
		else:
			raise Exception(f"'{className}' is not creatable!")
		
		Orientation._Memory.append(Object)
		Object.ClassName = className
		Object.Parent = parent
		Object.Name = className
		
		return Object

	def service(serviceName):
		if not hasattr(Orientation, serviceName):
			raise NotImplementedError(f"'{serviceName}' is not a valid service!")
		
		return Instance.new(serviceName, None, True)

# Initialize Services
workspace = Instance.service("Workspace")
PlayerGui = Instance.service("PlayerGui")