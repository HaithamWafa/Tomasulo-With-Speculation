""" created on Sunday Dec 3th 2019
@author: Mustafa Mahmoud """

class loader:
	def __init__(self):
		self.RS = [Reservation_Station() for i in range(2)]
		self.busy = False
		self.result = None
		self.cycle = 0

	def RS_empty(self):
		for station in self.RS:
			if station.busy is False:
				return 'YES'
		return 'NO'

	def issue(self, tag, opcode, s1_data, s1_tag, s2_data, s2_tag):
		for station in self.RS:
			if station.busy is False:
				if s1_tag == 'NA':
					vj = s1_data
					qj = None
					a = s1_data + s2_data
				else:
					vj = None
					qj = s1_tag
					a = s2_data
				station.issue(tag, opcode, vj, None, qj, None, a)
				return True
			return False

	def execute(self, instruction, RF, ROB, mem):
		if instruction.status == 'committed':
			base = RF.R[instruction.source1]
			offset = RF.R[instruction.immediate]
		else:
			for entry in ROB.entries:
				if entry.tag == instruction.dependency1:
					base = entry.result
			self.result = mem[base+offset]
			if self.busy == False:
				self.cycle = 0
				self.busy = True

	def incr_cycle(self):
		self.cycle += 1

	def khalasty(self):
		if self.cycle == 3:
			return 'YES'
		else:
			return 'NO'

	def write(self, instruction):
		if self.cycle == 3 and self.busy == True:
			result = self.result
		else:
			result = None
		self.busy = False
		for station in self.RS:
			if station.tag == instruction.tag:
				station.busy = False
				break
		return result