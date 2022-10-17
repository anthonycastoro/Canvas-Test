# Creates a new Signal (event dispatcher) 

class Signal:
	def __init__(self, invocation=False):
		self.Connections = []
		self.InvocationQueue = invocation and []
		self.InvocationEnabled = invocation
		self._Connection = None
	
	# Magic Methods
	
	__str__ = lambda self: "<Signal>"

	# Connection Class

	class _Connection:
		def __init__(self, event, callback):
			self.Connections = event.Connections
			self.Event = event
			self.Callback = callback
		
		Connected = True
		Event = None
		Connections = []
		Callback = lambda: None
		
		# Magic Methods #
			
		__str__ = lambda: "<Connection>"
		
		# Methods #
		
		def Disconnect(self):
			self.Connections.remove(self.Callback)
			self.Connected = False
			self.__str__ = lambda: "<Inactive Connection>"
	
	# Methods

	def Connect(self, callback):
		connection = Signal._Connection(self, callback)
		self.Connections.append(connection)
		
		if len(self.InvocationQueue or []) > 0:
			for params in self.InvocationQueue:
				self.Fire(*params)
			self.InvocationQueue.clear()
		
		return connection

	InvocationMax = 255
	def Fire(self, *Params):
		if len(self.Connections) == 0 and self.InvocationQueue:
			if len(self.InvocationQueue) >= self.InvocationMax:
				raise Exception(f"Did you forget to connect to this event? ({self.InvocationMax} events dropped)")
			self.InvocationQueue.append(Params)
		else:
			for connection in self.Connections:
				connection.Callback(*Params)