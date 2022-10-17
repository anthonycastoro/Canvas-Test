# Imports

import pygame as game
import os

from pygame import Color
from pygame.math import Vector2
from Common import *
import Enum
from Signal import Signal

# Instance Orientation

class Orientation:
	_TotalDebugId = 0

	# Base Class For Everything
	class Instance:
		_Creatiable = False
		_Service = False
		_ServiceCreated = False
		_Parent = None
		_Children = None
		_Changed = False
		_DebugId = 0
		_ClassIndex = 0
		_Locked = False
		
		Name = "Instance"
		ClassName = "Unknown"
		Destroyed = False
		
		ChildAdded = Signal()
		ChildRemoved = Signal()
		DescendantAdded = Signal()
		DescendantRemoved = Signal()
		Changed = Signal()
		
		__str__ = lambda self: self.Name

		def __init__(self):
			self._DebugId = Orientation._TotalDebugId
			Orientation._TotalDebugId += 1
			self._ServiceCreated = None
			self._Creatiable = None
			self._Children = []
			t = type(self)
			t._ClassIndex += 1

		@property
		def Parent(self):
			return self._Parent

		@Parent.setter
		def Parent(self, value):
			if (self._Service or self.Destroyed) and value != None: raise Exception(f"Parent is locked to None, attempt to set to '{value}'")
			if self._Locked: raise Exception(f"Parent property of '{self}' is locked.")
			
			if not (isinstance(value, Orientation.Instance) or value == None):
				raise AttributeError("Must set Parent to an Instance or None.")
			before = self._Parent
			self._Parent = value
			if before: before._Children.remove(self)
			if value: value._Children.append(self)
		
		@property
		def IsChangedThisFrame(self): return self._Changed
		
		def __getattr__(self, name):
			if not name in self.__dict__:
				for child in self._Children: # Allow indexing by child name
					if child.Name == name: return child
				raise AttributeError(f"'{self.Name}' has no attribute '{name}'!")
			else:
				return self.__dict__[name]
		
		def __setattr__(self, name, value):
			if hasattr(self, name) and getattr(self, name) != value and not name.startswith("_"): # Indicate if property has changed
				self._Changed = True
				self.Changed.Fire(name)
			elif not hasattr(self, name):
				raise AttributeError(f"'{self.Name}' has no settable attribute '{name}'!")
			super().__setattr__(name, value)

		def Destroy(self):
			if not self.Destroyed:
				self.Destroyed = True
				self.Parent = None
				
				if hasattr(self, "__destroy__"): self.__destroy__()
					
				for child in self._Children:
					child.Destroy()
				self._Children.clear()
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

		def GetClassIndex(self):
			return self._ClassIndex
			
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
				Instance._fixImmutableAttributes(cloned)
				return cloned
			else:
				raise Exception(f"Cannot clone Service '{self.ClassName}'")

	# Services
	class Workspace (Instance):
		_Creatiable = False
		_Service = True
		_AwakeParts = []
		_CurrentCamera = None
		
		SkyColor = Color(125,125,255)
		Gravity = 100
		FPS = 0
		MasterVolume = 1
		VoidDepth = 20
		PlanckLength = 0.01
		
		@property
		def CurrentCamera(self):
			return self._CurrentCamera

		@CurrentCamera.setter
		def CurrentCamera(self, value):
			if type(value) == Orientation.Camera or value == None:
				self._CurrentCamera = value
			else:
				raise AttributeError(f"CurrentCamera must be a Camera. Got a '{type(value).__name__}'")


	class PlayerGui (Instance):
		_Creatiable = False
		_Service = True

		Debug = True

	# Misc Instances
	class Player (Instance):
		_Creatiable = True
		
		Character = None
		Score = 0
		LivesLost = -1
		UserColor = Color(0,240,0)
		Health = 100
		DisplayName = os.environ["REPL_OWNER"]

	class Camera (Instance):
		_Creatiable = True
		
		Position = Vector2(2,2)
		Roll = 0
		Zoom = 4
		ZoomIncrement = 50
		ZoomRange = Vector2(2, 150)
		Speed = Vector2(7,7)
		Mode = Enum.CameraMode.Debug
			
	# Abstract Classes
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
		Anchored = True
		CanCollide = True

		AbsoluteCorner = Vector2()
		AbsoluteSize = Vector2(100,100)
		AbsoluteCenter = Vector2(50,50)
				
		def __init__(self):
			super().__init__()
			workspace._AwakeParts.append(self)

		def __destroy__(self):
			workspace._AwakeParts.remove(self)

		def GetRect(self):
			planck = workspace.PlanckLength
			p = Vector2(self.Position.x, -self.Position.y) / planck
			s = self.Size / planck
			return game.Rect(p - s/2, s)

		def Crush(self):
			self.Destroy()
		
	# Invisible Instances
	
	class Sound (Instance):
		_Creatiable = True
		_IsPlaying = False
		_Path = ""
				
		_Mixer = None
		_Channel = None
		Playing = False
		Paused = False
		Looped = False
		Volume = 1
		Pan = 0

		Length = 0
		
		MaxDistance = 20
		MinDistance = 0

		@property
		def Path(self):
			return self._Path

		@Path.setter
		def Path(self, value):
			if self._Mixer: self._Mixer.stop()
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
			self._Mixer = game.mixer.Sound(p)
			self._Mixer.stop()
			self.Length = self._Mixer.get_length()
			self._Path = value

		@property
		def PlaybackLoudness(self):
			return self._Channel.get_volume()
		
		def __init__(self):
			super().__init__()
			self._Channel = game.mixer.Channel(self.GetClassIndex())
		
		def Play(self, wait=0):
			if self._Mixer:
				if wait != 0:
					return delay(self.Play, wait)
				self._Channel.play(self._Mixer)
				self.Playing = True
				self._IsPlaying = True
		
		def Stop(self):
			if self._IsPlaying:
				self.Playing = False
				if self._Mixer:
					self._Channel.stop()
					self._IsPlaying = False
		
		# Update
		
		def Update(self, dt, window):
			if self._Mixer and self._Channel:
				# Playing Check

				if not self.Playing and self._IsPlaying:
					self.Stop()
				
				# Paused Check
				
				if self.Paused:
					self._Channel.pause()
				else:
					self._Channel.unpause()

				# Volume and Pan Check

				def SetPan(pan, multi=1):
					pan = (pan + 1) / 2 # 0 to 1 instead of -1 to 1
					if pan < 0: pan = 0
					if pan > 1: pan = 1
					multi *= workspace.MasterVolume
					self._Channel.set_volume((1 - pan) * multi, pan * multi)
					
				if self.Playing:
					if not self.Parent:
						SetPan(self.Pan, self.Volume)
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
						SetPan(p, multi * self.Volume)

				# Loop Check
				if not self._Channel.get_busy():
					if self.Looped and self._IsPlaying and self.Playing:
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
		_Font = None
		_FaceName = "Arial"
				
		Text = "Label Text" 
		TextTransparency = 0 
		TextSize = 14 
		TextScaled = False 
		TextColor = Color(0,0,0) 
		TextWrapped = False # TODO: Work with TextScaled and Center YAlignment
		AntiAlias = True
		LineHeight = 0.5
		TextXAlign = Enum.TextXAlign.Center
		TextYAlign = Enum.TextYAlign.Center
		
		Bold = False
		Italic = False
		Underline = False

		# Read Only
		
		TextFits = True
		TextBounds = Vector2()

		if not game.font.get_init(): game.font.init()
		
		def GetFontFace(self, name, size):
			return game.font.Font(f"Font/{name.lower()}.ttf", size)
		_Font = GetFontFace(None, "Arial", TextSize)
		
		def __setattr__(self, name, value):
			super().__setattr__(name, value)
			if name == "TextSize" or name == "Font" or name == "TextScaled":
				self._Font = self.GetFontFace(self._FaceName, 
					self.TextScaled and 50 or self.TextSize)
		
		def RenderTextWrapping(self, surface):
			text = self.Text
			font = self._Font
			maxwidth = surface.get_width() - 4
			maxheight = surface.get_height() - 4

			words = text.split()
			lines = []
			
			while len(words) > 0:
				line_words = []
				while len(words) > 0:
					word = words.pop(0).strip()
					
					line_words.append(word)
					fw, _ = font.size(' '.join(line_words + words[:1]))
					if fw > maxwidth:
						break
		
				lines.append(' '.join(line_words))

			y_offset = 0
			sw = surface.get_width()
			texts = []
			linesize = font.get_linesize() * self.LineHeight
			for line in lines:
				text = font.render(line, self.AntiAlias, self.TextColor)
				addition = text.get_height() + linesize
				if y_offset + addition > maxheight: 
					self.TextFits = False
					break
				texts.append([text, y_offset])
				y_offset += addition
			
			labelsurface = game.Surface((sw, surface.get_height()), game.SRCALPHA).convert_alpha()
			labelsurface.fill(Color(0,0,0,0))
			
			for text in texts:
				surf = text[0]
				y = text[1]
				rect = surf.get_rect()
				labelrect = labelsurface.get_rect()
				
				if self.TextXAlign == Enum.TextXAlign.Center:
					rect.center = labelrect.center
				elif self.TextXAlign == Enum.TextXAlign.Left:
					rect.left = labelrect.left + 2
				elif self.TextXAlign == Enum.TextXAlign.Right:
					rect.right = labelrect.right - 2
	
				if self.TextYAlign == Enum.TextYAlign.Center:
					rect.top = y + (labelrect.bottom - y_offset + surf.get_height()) / 2
				elif self.TextYAlign == Enum.TextYAlign.Top:
					rect.top = y
				elif self.TextYAlign == Enum.TextYAlign.Bottom:
					rect.top = y + labelrect.bottom - y_offset
				
				surf.set_alpha(toAlpha(self.TextTransparency))
				labelsurface.blit(surf, rect)
			
			surface.blit(labelsurface, (0,0))
		
		def Render(self, surface, dt):
			super().Render(surface, dt)
			font = self._Font
			font.bold = self.Bold
			font.italic = self.Italic
			font.underline = self.Underline

			self.TextFits = True
			if self.TextWrapped:
				self.RenderTextWrapping(surface)
			else:
				text = font.render(self.Text, self.AntiAlias, self.TextColor)
				if self.TextScaled:
					text = AspectRatioScale(text, surface.get_width(), surface.get_height())
				rect = text.get_rect()
				labelrect = surface.get_rect()
				
				if self.TextXAlign == Enum.TextXAlign.Center:
					rect.centerx = labelrect.centerx
				elif self.TextXAlign == Enum.TextXAlign.Left:
					rect.left = labelrect.left + 2
				elif self.TextXAlign == Enum.TextXAlign.Right:
					rect.right = labelrect.right - 2
	
				if self.TextYAlign == Enum.TextYAlign.Center:
					rect.centery = labelrect.centery
				elif self.TextYAlign == Enum.TextYAlign.Top:
					rect.top = labelrect.top + 2
				elif self.TextYAlign == Enum.TextYAlign.Bottom:
					rect.bottom = labelrect.bottom - 2
				
				self.TextBounds = Vector2(text.get_width(), text.get_height())
				text.set_alpha(toAlpha(self.TextTransparency))
				surface.blit(text, rect)
				if text.get_width() > surface.get_width() or text.get_height() > surface.get_height():
					self.TextFits = False		

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
			raise Exception("Cannot create a service!")
		elif service and Creator._ServiceCreated:
			return Instance.services[className]
		elif Creator._Service and service:
			Creator._ServiceCreated = True
		
		if Creator._Creatiable or (service and Creator._Service):
			Object = Creator()
			if service: Instance.services[className] = Object
		else:
			raise Exception(f"'{className}' is not creatable!")
		
		Object.ClassName = className
		Object.Name = className
		Instance._fixImmutableAttributes(Object)
		Object.Parent = parent
		return Object

	def service(serviceName):
		if not hasattr(Orientation, serviceName):
			raise NotImplementedError(f"'{serviceName}' is not a valid service!")
		
		return Instance.new(serviceName, None, True)

	def _fixImmutableAttributes(Object):
		for i in dir(Object):
			v = getattr(Object, i)
			if type(v) == Signal:
				setattr(Object, i, Signal(v.InvocationEnabled))
			if type(v) == Vector2:
				setattr(Object, i, Vector2(v.x, v.y))
			if type(v) == Color:
				setattr(Object, i, Color(v.r, v.g, v.b, v.a))

# Initialize Services

workspace = Instance.service("Workspace")
PlayerGui = Instance.service("PlayerGui")
workspace.CurrentCamera = Instance.new("Camera", workspace)

# Run Scripts

for script in os.listdir("Scripts"):
	if script.endswith(".py"):
		spawn(lambda: exec("from Scripts import " + script[:-3]))