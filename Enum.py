# Lists different options used for properties

class EnumItem:
	def __init__(self, Value=0):
		self.Value = Value

	__str__ = lambda self: f"Enum.{self.EnumType.Name}.{self.Name}"
	
	Value = 0
	@property
	def Name(self):
		for name, enumitem in vars(self.EnumType).items():
			if enumitem == self:
				return name
		raise IndexError("Cannot find name of EnumItem.")
	@property
	def EnumType(self):
		return type(self).__bases__[0]

class EnumType:
	@property
	def Name(self):
		return type(self).__name__

class TextXAlign (EnumType):
	Left = EnumItem(0)
	Center = EnumItem(0.5)
	Right = EnumItem(1)

class TextYAlign (EnumType):
	Top = EnumItem(0)
	Center = EnumItem(0.5)
	Bottom = EnumItem(1)