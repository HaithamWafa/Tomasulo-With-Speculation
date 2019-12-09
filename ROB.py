""" created on Sunday Dec 8th 2019
@author: Mustafa Mahmoud """

#NOTE: THIS ROB SUPPORTS SINGLE ISSUE ONLY

class ROBentry:
    def __init__(self):
    	self.ROBentry = None
        self.empty = True
        self.done = False
        self.tag = None
        self.result = None

    def WriteInst(self, instruction, InstNumber):
     	self.ROBentry = instruction
     	self.empty = False
     	self.tag = InstNumber

    def ClearEntry(self):
     	self.ROBentry = None
        self.empty = True
    
    def InstCompleted(self, result):
    	self.done = Tru
    	self.result = result

    def print_entry():
    	print(self.ROBentry, '\t', self.empty, '\t', self.done, '\t', self.tag, '\t', self.result)

class ROB:
	NofEntries = 0
	def __init__(self, NofEntries):
		self.entries = [ROBentry() for i in range(NofEntries)]
		self.head = 0
		self.tail = 0
		self.full = False
		self.NofEntries = NofEntries

	def write(self, instruction, InstNumber):
		if self.entries[self.head].empty:
			self.entries[self.head].WriteInst(instruction, InstNumber)
			if self.head < self.NofEntries:
				self.head += self.head
			else:
				self.head = 0
		else:
			self.full = True
			print("ROB is full, stop issuing")

	def CompleteInst(self, result, InstNumber):
		for entry in self.entries:
			if entry.tag == InstNumber:
				entry.InstCompleted(result)
				break

	def commit(self):
		if self.entries[self.tail].empty == False && self.entries[self.tail].done == True:
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
		return how_many

	def print_all_entries():
		for entry in self.entries:
			entry.print_entry()