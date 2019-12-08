""" created on Sunday Dec 8th 2019
@author: Mustafa Mahmoud """

#NOTE: THIS ROB SUPPORTS SINGLE ISSUE ONLY

class ROBentry:
    def __init__(self):
    	self.ROBentry = None
        self.empty = True
        self.exception = False	#to indicate if an instruction throws an exception

    def WriteInst(self, instruction, exception):
     	self.ROBentry = instruction
     	self.empty = False
     	self.exception = exception

    def ClearEntry(self):
     	self.ROBentry = None
        self.empty = True
        self.exception = False


class ROB:
	def __init__(self, NofEntries):
		self.entries = [ROBentry() for i in range(NofEntries)]
		self.head = 0
		self.tail = 0
		self.full = False

	def write(self, instruction):
		if self.entries[self.head].empty:
			self.entries[self.head].WriteInst(instruction)
			if self.head < self.NofEntries:
				self.head += self.head
			else:
				self.head = 0
		else:
			self.full = True
			print("ROB is full, stop issuing")

	def commit(self):		#WARNING! This method raises a nameerror exception
		if self.entries[self.tail].empty is False:
			if self.entries[self.tail].exception:
				raise NameError('Exception!')
			else:
				self.entries[self.tail].ClearEntry()
				self.full = False
				if self.tail < self.NofEntries:
					self.tail += self.tail
				else:
					self.tail = 0
		else:
			print("Nothing to commit")

