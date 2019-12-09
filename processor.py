# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 19:24:23 2019

@author: Haitham Samir
"""

class Reservation_Station:
  def __init__(self):
    self.tag = None
    self.busy= False
    self.opcode= None
    self.vj= None
    self.vk= None
    self.qj= None
    self.qk= None
    self.a= None

  def issue(self, tag, opcode, vj, vk, qj, qk, a):
    self.busy = True
    self.opcode = opcode
    self.tag = tag
    self.a = a
    if qj == None:
        self.vj = vj
    else:
        self.qj = qj
        self.vj = None
    if qk == None:
        self.vk = vk
    else:
        self.qk = qk
        self.vk = None

  def update(self, vj, vk):
    if vj != None:
      self.vj = vj
      self.qj = None
    if vk != None:
      self.vk = vk
      self.qk = None

  def clear(self)
    self.tag = None
    self.busy= False
    self.opcode= None
    self.vj= None
    self.vk= None
    self.qj= None
    self.qk= None
    self.a= None

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
    	self.done = True
    	self.result = result

    def print_entry(self):
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
		if self.entries[self.tail].empty == False and self.entries[self.tail].done == True:
			self.entries[self.tail].ClearEntry()
			self.full = False
			if self.tail < self.NofEntries:
				self.tail += self.tail
			else:
				self.tail = 0
		else:
			print("Nothing to commit.")

	def empty_entries(self):
		how_many = 0
		for entry in self.entries:
			if entry.empty:
				how_many += how_many
		return how_many

	def print_all_entries(self):
		for entry in self.entries:
			entry.print_entry()


class instruction:
     def __init__(self):
            self.instType = 'ADD'         
            self.destination = 'R0'
            self.source1 = 'R0'
            self.source2 = 'R0'
            self.immediate = 0
            self.tag = 0
            self.functional_unit = 'NA'
            self.issued = 'NO'
     
          
            
def Import_Instruction_File():
#   instFile= open("Instructions.txt","w+")       #opening instructions file for writing
#    
#   for i in range(15):
#     instFile.write("ADD R0, R0, R0 \n")              #writing instructions
#     
#   instFile.close() 
    instFile= open("Instructions.txt","r+")    #opening instructions file for reading
    lines=instFile.readlines()               #this reads all lines into a list
    instFile.close() 
    while(1):
        try:
            lines.remove('\n')
        except ValueError:
            break            
    return lines;    
def Parse_Instructions(instructions):
    
    inst = [None]*(len(instructions))
     
    for i in range(len(instructions)):   #parsing the instructions read
       inst[i]=instructions[i].split()
       instructions[i]=instruction() 
       instructions[i].tag=i   #setting the instruction order 
       instructions[i].instType=inst[i][0]   #setting the type of instruction
       if(inst[i][0]== 'ADD' or inst[i][0]== 'SUB' or inst[i][0]== 'NAND' or inst[i][0]== 'MUL'):
          instructions[i].destination=inst[i][1]
          instructions[i].source1=inst[i][2]
          instructions[i].source2=inst[i][3]
          instructions[i].immediate='NA'
       elif (inst[i][0]== 'LW'):
          instructions[i].destination=inst[i][1]
          instructions[i].source1=inst[i][2]
          instructions[i].source2='NA'
          instructions[i].immediate=inst[i][3]
       elif (inst[i][0]== 'SW'):
          instructions[i].source1=inst[i][1]
          instructions[i].source2=inst[i][2]
          instructions[i].immediate=inst[i][3]
          instructions[i].destination='NA'
       elif (inst[i][0]== 'BEQ'):
          instructions[i].source1=inst[i][1]
          instructions[i].source2=inst[i][2]
          instructions[i].immediate=inst[i][3]
          instructions[i].destination='NA'
       elif (inst[i][0]== 'JMP'):
          instructions[i].source1='NA'
          instructions[i].source2='NA'
          instructions[i].destination='NA'
          instructions[i].immediate=inst[i][1]   
       elif (inst[i][0]== 'JALR'):
          instructions[i].source1=inst[i][1]
          instructions[i].source2='NA'
          instructions[i].destination='NA'
          instructions[i].immediate='NA'
       elif (inst[i][0]== 'RET'):
          instructions[i].source1='NA'
          instructions[i].source2='NA'
          instructions[i].destination='NA'
          instructions[i].immediate='NA'
       elif(inst[i][0]== 'ADDI'):
          instructions[i].destination=inst[i][1]
          instructions[i].source1=inst[i][2]
          instructions[i].source1='NA'
          instructions[i].immediate=inst[i][3]
       else:
          print("INCORRECT INSTRUCTION")
          
        
    for i in range (len(instructions)):  #cleaning up
       instructions[i].source1 = instructions[i].source1.strip(',')
       instructions[i].source2 = instructions[i].source2.strip(',')
       instructions[i].destination = instructions[i].destination.strip(',')