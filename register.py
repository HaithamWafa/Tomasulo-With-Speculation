class register:
    def __init__(self):
        self.data = 0
        self.tag = None

    def issue(self, tag):
    	self.tag = tag

    def write(self, data):
    	self.data = data
    	self.tag = None

class RegFile:
	def __init__(self):
		self.R = {'R0': register(), 'R1': register(), 'R2': register(), 'R3': register(), 'R4': register(), 'R5': register(), 'R6': register(), 'R7': register()}

	def issue(self, RegNo, tag):
		self.R[RegNo].issue(tag)

	def write(self, RegNo, data):
		self.R[RegNo].write(data)