""" created on Sunday Dec 10th 2019
@author: Mustafa Mahmoud """

class mul:
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
				else:
					vj = None
					qj = s1_tag
				if s2_tag == 'NA':
					vk = s2_data
					qk = None
				else:
					vk = None
					qk = s2_tag
				station.issue(tag, opcode, vj, vk, qj, qk, None)
				return True
			return False

	def execute(self, instruction, RF, ROB):
		if instruction.status == 'committed':
			src1 = RF.R[instruction.source1]
			src2 = RF.R[instruction.source2]
		else:
			for entry in ROB.entries:
				if entry.tag == instruction.dependency1:
					src1 = entry.result
				elif entry.tag == instruction.dependency2:
					src2 = entry.result
			self.result = src1 * src2
			if self.busy == False:
				self.cycle = 0
				self.busy = True

	def incr_cycle(self):
		self.cycle += 1

	def khalasty(self):
		if self.cycle == 10:
			return 'YES'
		else:
			return 'NO'

	def write(self, instruction):
		if self.cycle == 10 and self.busy == True:
			result = self.result
		else:
			result = None
		self.busy = False
		for station in self.RS:
			if station.tag == instruction.tag:
				station.busy = False
				break
		return result