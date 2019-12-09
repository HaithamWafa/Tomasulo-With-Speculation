""" created on Sunday Dec 8th 2019
@author: Mustafa Mahmoud """

#NOTE: THIS ROB SUPPORTS SINGLE ISSUE ONLY

class ROBentry:
    def __init__(self):
    	self.ROBentry = None
        self.empty = True
        self.exception = False	#to indicate if an instruction throws an exception
        self.done = False
        self.tag = None
        self.result - None

    def WriteInst(self, instruction, InstNumber):
     	self.ROBentry = instruction
     	self.empty = False
     	self.tag = InstNumber

    def ClearEntry(self):
     	self.ROBentry = None
        self.empty = True
        self.exception = False
    
    def InstCompleted(self, exception, result):
    	self.done = True
    	self.exception = exception
    	self.result = result


class ROB:
	NofEntries = 0
	def __init__(self, NofEntries):
		self.entries = [ROBentry() for i in range(NofEntries)]
		self.head = 0
		self.tail = 0
		self.full = False
		self.NofEntries = NofEntries

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

	def CompleteInst(self, exception, result, InstNumber):
		for entry in self.entries:
			if entry.tag == InstNumber:
				entry.InstCompleted(exception, result)
				break

	def commit(self):		#WARNING! This method raises a nameerror exception
		if self.entries[self.tail].empty == False && self.entries[self.tail].done == True:
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
			print("Nothing to commit.")

	def empty_entries():
		how_many = 0
		for entry in self.entries:
			if entry.empty:
				how_many += how_many