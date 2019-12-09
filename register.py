class register:
    def __init__(self):
        self.data = None
        self.tag = None

    def issue(self, tag):
    	self.tag = tag

    def write(self, data):
    	self.data = data
    	self.tag = None

class RegFile:
	def __init__(self):
		self.R = [register() for i in range(7)]

	def issue(self, RegNo, tag):
		self.R[RegNo].issue(tag)

	def write(self, RegNo, data):
		self.R[RegNo].write(data)