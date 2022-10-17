import pygame as game

class EnumItem:
	_Closed = False
	
	Value = -1
	Name = "Unknown"
	EnumType = None
	
	def __init__(self, name, value, type):
		if self._Closed: raise Exception("Cannot create custom EnumItem!")
		self.Value = value
		self.Name = name
		self.EnumType = type
	
	def __str__(self):
		return f"Enum.{self.EnumType.Name}.{self.Name}"

	def __eq__(self, other):
		val = False
		try: val = str(Reveal(self.EnumType, other)) == str(self)
		finally: return val

Types = []
class EnumType:
	Name = "Option"
	_Items = {}
	_DebugId = 0
	_Closed = False
	
	def __init__(self, name="Option"):
		if self._Closed: raise Exception("Cannot create custom EnumType!")
		global Types
		EnumType._DebugId += 1
		self.Name = name
		self._Items = {}
		Types.append(self)

	def add(self, *args, **pairs):
		if self._Closed: raise Exception("This enum is now read only.")
		for name in args:
			self._Items[name] = EnumItem(name, len(self._Items), self)
		for name, value in pairs.items():
			self._Items[name] = EnumItem(name, value, self)
		return self

	def GetEnumItems(self):
		return self._Items

	def GetItemById(self, id):
		for item in self._Items.values():
			if item.Value == id:
				return item
	
	__str__ = lambda self: "Enum." + self.Name

	def __getattr__(self, name):
		if name in self._Items:
			return self._Items[name]
		else:
			raise AttributeError(f"Enum.{self.Name}.{name} does not exist!")

	def __setattr__(self, name, value):
		if self._Closed:
			raise AttributeError(f"Enum.{self.Name} is read only!")
		else: self.__dict__[name] = value

# Enums

TextXAlign = EnumType("TextXAlign").add("Left", "Center", "Right")
TextYAlign = EnumType("TextYAlign").add("Top", "Center", "Bottom")

CameraMode = EnumType("CameraMode").add("Debug", "Subject", "Scriptable")
KeyCode = EnumType("KeyCode")

# KeyCodes

CodeAlias = {
	"Lctrl": "LeftControl",
	"Lshift": "LeftShift",
	"Lalt": "LeftAlt",
	"Rctrl": "RightControl",
	"Rshift": "RightShift",
	"Ralt": "RightAlt",
	"Rightparen": "RightParen",
	"Leftparen": "LeftParen",
	"Rightbracket": "RightBracket",
	"Leftbracket": "LeftBracket",
	"Rightbrace": "RightBrace",
	"Leftbrace": "LeftBrace",
	"Capslock": "CapsLock",
	"Numlock": "NumLock",
	"Scrolllock": "ScrollLock",
	"Semicolon": "SemiColon",
	"Pagedown": "PageDown",
	"PageUp": "PageUp",
	"Hash": "Hashtag",
	"Lmeta": "LeftSpecial",
	"Rmeta": "RightSpecial",
}
RemovedCodes = [
	"Ac_Back", "Rgui", "Lgui",
	"Lsuper", "Rsuper", "Mode",
	"Currencysubunit", "Numlockclear",
	"Help", "Sysreq", "Menu",
	"Currencyunit"
]

for name, id in game.__dict__.items():
	if name.startswith("K_"):
		code = name[2:].title()
		if code.startswith("KP") and not code.startswith("KP_"): continue
		if code in RemovedCodes: continue
		
		numpad = code.startswith("KP_") and "Numpad" or ""
		code = code.replace("KP_", "")
		
		if code in "0123456789":
			code = numpad + "Zero One Two Three Four Five Six Seven Eight Nine".split()[int(code)]
		
		if code in CodeAlias:
			code = CodeAlias[code]

		KeyCode.add(**{code: id})

# Close Enum Creation

for t in Types: t._Closed = True
Types = None
EnumType._Closed = True
EnumItem._Closed = True

# Global Methods

def Reveal(enum, value): # Attempts to convert any value to an EnumItem
	if type(value) == int or type(value) == float:
		return enum.GetItemById(value)
	if type(value) == EnumItem: return value
	if type(value) == str:
		for item in enum._Items.values():
			if item.Name.lower() == value.lower(): return item
	raise AttributeError(f"Expected an Item of '{enum}'. Got '{value}'")