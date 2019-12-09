# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 11:24:17 2019

@author: Haitham Samir
"""
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
    
def main():
    
   instructions = Import_Instruction_File() #imports instructions as a list of strings
   Parse_Instructions(instructions)
   
   print(instructions[1].destination)   #used for testing  
   
 #  issue_cycles=0
   #issuing loop
#   for i in range(len(instructions)-1):
#       if(instructions[i].functional_unit.reservation_station.busy == 'NO' and instructions[i+1].functional_unit.reservation_station.busy and ROB.available_entries == 2):
#           instructions[i].issued = 'YES'
#           instructions[i+1].issued = 'YES'
#           issue_cycles=issue_cycles+1
  # I = instruction()
   R = ROB(16)
   R.write(instructions[1 ].destination, 1)
   R.CompleteInst(33, 1)
   #R.commit()
   R.print_all_entries()

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    