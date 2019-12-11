class FU:
	def __init__(self):
		self.adder = adder()
		self.multiplier = mul()
		self.brancher = brancher()
		self.Nand = Nand()
		self.jmp = jmp()
		self.loader = loader()
		self.storer = storer()
		self.RF = RegFile()
		self.mem = [0 for i in range(1023)]

	def issue(self, instruction):
		if instruction.instType == 'ADD' or instruction.instType == 'SUB':
			self.adder.issue(instruction.tag, instruction.instType, self.RF.R[instruction.source1].data, instruction.dependency1, self.RF.R[instruction.source1].data, instruction.dependency2)
		elif instruction.instType == 'ADDI':
			self.adder.issue(instruction.tag, instruction.instType, self.RF.R[instruction.source1].data, instruction.dependency1, instruction.immediate, instruction.dependency2)
		elif instruction.instType == 'MUL':
			self.adder.issue(instruction.tag, instruction.instType, self.RF.R[instruction.source1].data, instruction.dependency1, self.RF.R[instruction.source1].data, instruction.dependency2)
		elif instruction.instType == 'LW':
			self.loader.issue(instruction.tag, instruction.instType, self.RF.R[instruction.source1].data, instruction.dependency1, instruction.immediate, None)
		elif instruction.instType == 'SW':
			self.storer.issue(instruction.tag, instruction.instType, self.RF.R[instruction.source2].data, instruction.dependency2, instruction.immediate, None)
		elif instruction.instType == 'BEQ':
			pass
			#self.brancher.issue()
		elif instruction.instType == 'JMP' or instruction.instType == 'JALR' or instruction.instType == 'RET':
			pass
			#self.jmp.issue()
		elif instruction.instType == 'NAND':
			self.Nand.issue(instruction.tag, instruction.instType, self.RF.R[instruction.source1].data, instruction.dependency1, self.RF.R[instruction.source1].data, instruction.dependency2)
	
	def execute(self, instruction):
		if instruction.instType == 'ADD' or instruction.instType == 'SUB':
			self.adder.execute(instruction, self.RF, ROB)
		elif instruction.instType == 'ADDI':
			self.adder.execute(instruction, self.RF, ROB)
		elif instruction.instType == 'MUL':
			self.multiplier.execute(instruction, self.RF, ROB)
		elif instruction.instType == 'LW':
			self.loader.execute(instruction, self.RF, ROB, self.mem)
		elif instruction.instType == 'SW':
			self.storer.execute(instruction, self.RF, ROB, self.mem)
		elif instruction.instType == 'BEQ':
			pass
			#self.brancher.execute(instruction, self.RF, ROB)
		elif instruction.instType == 'JMP' or instruction.instType == 'JALR' or instruction.instType == 'RET':
			pass
			#self.jmp.execute(instruction, self.RF, ROB)
		elif instruction.instType == 'NAND':
			self.Nand.execute(instruction, self.RF, ROB)
		instruction.dependency1 = 'NA'
		instruction.dependency2 = 'NA'

	def result(self, instruction):
		if instruction.instType == 'ADD' or instruction.instType == 'SUB':
			return self.adder.write(instruction)
		elif instruction.instType == 'ADDI':
			return self.adder.write(instruction)
		elif instruction.instType == 'MUL':
			return self.multiplier.write(instruction)
		elif instruction.instType == 'LW':
			return self.loader.write(instruction)
		elif instruction.instType == 'SW':
			return self.storer.write(instruction)
		elif instruction.instType == 'BEQ':
			return None
			#return self.brancher.write(instruction)
		elif instruction.instType == 'JMP' or instruction.instType == 'JALR' or instruction.instType == 'RET':
			return None
			#return self.jmp.write(instruction)
		elif instruction.instType == 'NAND':
			return self.Nand.write(instruction)
	
	def khalasty(self, instruction):
		if instruction.instType == 'ADD' or instruction.instType == 'SUB':
			return self.adder.khalasty()
		elif instruction.instType == 'ADDI':
			return self.adder.khalasty()
		elif instruction.instType == 'MUL':
			return self.multiplier.khalasty()
		elif instruction.instType == 'LW':
			return self.loader.khalasty()
		elif instruction.instType == 'SW':
			return self.storer.khalasty()
		elif instruction.instType == 'BEQ':
			return 'YES'
			#return self.brancher.khalasty()
		elif instruction.instType == 'JMP' or instruction.instType == 'JALR' or instruction.instType == 'RET':
			return 'YES'
			#return self.jmp.khalasty()
		elif instruction.instType == 'NAND':
			return self.Nand.khalasty()
	
	def check_relevent_RS(self, instruction):
		if instruction.instType == 'ADD' or instruction.instType == 'SUB':
			return self.adder.RS_empty()
		elif instruction.instType == 'ADDI':
			return self.adder.RS_empty()
		elif instruction.instType == 'MUL':
			return self.multiplier.RS_empty()
		elif instruction.instType == 'LW':
			return self.loader.RS_empty()
		elif instruction.instType == 'SW':
			return 'YES'
			#return self.storer.RS_empty()
		elif instruction.instType == 'BEQ':
			return 'YES'
			#return self.brancher.RS_empty()
		elif instruction.instType == 'JMP' or instruction.instType == 'JALR' or instruction.instType == 'RET':
			return self.jmp.RS_empty()
		elif instruction.instType == 'NAND':
			return self.Nand.RS_empty()
	
	def IncrClk(self):
		self.adder.incr_cycle()
		self.multiplier.incr_cycle()
		#self.brancher.incr_cycle()
		self.Nand.incr_cycle()
		#self.jmp.incr_cycle()
		self.loader.incr_cycle()
		self.storer.incr_cycle()
	
	def commit(self, result, tag):
		for R in self.RF.R:
			if R.tag == tag:
				R.data = result
				break