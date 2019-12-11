# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 19:24:23 2019

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
      if self.head < self.NofEntries-1:
        self.head += 1
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
      x = self.entries[self.tail].tag
      self.entries[self.tail].ClearEntry()
      self.full = False
      if self.tail < self.NofEntries-1:
        self.tail += 1
      else:
        self.tail = 0
      return x
    else:
      return None

  def empty_entries(self):
    how_many = 0
    for entry in self.entries:
        if entry.empty:
            how_many += 1
    if how_many > 0:
        return 'YES'
    return 'NO'

  def print_all_entries(self):
    for entry in self.entries:
      entry.print_entry()


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

    def clear(self):
        self.tag = None
        self.busy= False
        self.opcode= None
        self.vj= None
        self.vk= None
        self.qj= None
        self.qk= None
        self.a= None

class adder:
  def __init__(self):
    self.RS = [Reservation_Station() for i in range(2)]
    self.busy = False
    self.result = None
    self.cycle = 0
    self.test_variable = 0

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
    if instruction.dependency1 == 'NA':
      src1 = RF.R[instruction.source1].data
    else:
      for entry in ROB.entries:
        print('This is source 1 dependecy', instruction.dependency1)
        print('these are rob entry tags ------>>', entry.tag)
        if entry.tag == instruction.dependency1:
          src1 = entry.result
          print('source 1 inside adder execute', src1)
          break
    if instruction.dependency2 == 'NA':
        if instruction.instType == 'ADDI':
            src2 = int(instruction.immediate)
            self.test_variable += 1
            print('Test Variable -->', self.test_variable)
        else:
            src2 = RF.R[instruction.source2].data
    else:
      for entry in ROB.entries:
        if entry.tag == instruction.dependency2:
          src2 = entry.result
          break
    print(self.cycle)
    #if self.cycle == 2:
    if instruction.instType == 'SUB':
        self.result = src1 - src2
        print('I computed the SUB and the result is =>', self.result)
    else:
        self.result = src1 + src2
    if self.busy == False:
        self.cycle = 0
        self.busy = True

  def incr_cycle(self):
    self.cycle += 1
    #print('this is addi cycle', self.cycle)

  def khalasty(self):
    if self.cycle >= 2:
        #print('addi 5aallast yabo el cabaten!!')
        return 'YES'
    else:
      #print('addi lessa yabo el cabaten!!')  
      return 'NO'

  def write(self, instruction):
    if self.cycle >= 2 and self.busy == True:
      result = self.result
    else:
      result = None
    self.busy = False
    for station in self.RS:
      if station.tag == instruction.tag:
        station.busy = False
        break
    return result

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
          a = int(s1_data) + int(s2_data)
        else:
          vj = None
          qj = s1_tag
          a = s2_data
        station.issue(tag, opcode, vj, None, qj, None, a)
        return True
      return False

  def execute(self, instruction, RF, ROB, mem):
    offset = int(instruction.immediate)
    if instruction.dependency1 == 'NA':
      base = RF.R[instruction.source1].data
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
    if self.cycle >= 3:
      return 'YES'
    else:
      return 'NO'

  def write(self, instruction):
    if self.cycle >= 3 and self.busy == True:
      result = self.result
    else:
      result = None
    self.busy = False
    for station in self.RS:
      if station.tag == instruction.tag:
        station.busy = False
        break
    return result

class storer:
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
          a = int(s1_data) + int(s2_data)
        else:
          vj = None
          qj = s1_tag
          a = s2_data
        station.issue(tag, opcode, vj, None, qj, None, a)
        return True
      return False

  def execute(self, instruction, RF, ROB, mem):
    offset = int(instruction.immediate)
    X = RF.R[instruction.source1].data
    if instruction.dependency1 == 'NA':
      base = RF.R[instruction.source2].data
    else:
      for entry in ROB.entries:
        if entry.tag == instruction.dependency1:
          base = entry.result
    print(entry.result, '<-- This is base data')
    mem[base+offset] = X
    if self.busy == False:
        self.cycle = 0
        self.busy = True

  def incr_cycle(self):
    self.cycle += 1

  def khalasty(self):
    if self.cycle >= 3:
      return 'YES'
    else:
      return 'NO'

  def write(self, instruction):
    if self.cycle >= 3 and self.busy == True:
      result = self.result
    else:
      result = None
    self.busy = False
    for station in self.RS:
      if station.tag == instruction.tag:
        station.busy = False
        break
    return result

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
    if instruction.dependency1 == 'NA':
      src1 = RF.R[instruction.source1]
    else:
      for entry in ROB.entries:
        if entry.tag == instruction.dependency1:
          src1 = entry.result
          break
    if instruction.dependency2 == 'NA':
      src2 = RF.R[instruction.source2]
    else:
      for entry in ROB.entries:
        if entry.tag == instruction.dependency2:
          src2 = entry.result
          break
    if self.cycle == 10:
        self.result = src1 * src2
    if self.busy == False:
        self.cycle = 0
        self.busy = True

  def incr_cycle(self):
    self.cycle += 1

  def khalasty(self):
    if self.cycle >= 10:
      return 'YES'
    else:
      return 'NO'

  def write(self, instruction):
    if self.cycle >= 10 and self.busy == True:
      result = self.result
    else:
      result = None
    self.busy = False
    for station in self.RS:
      if station.tag == instruction.tag:
        station.busy = False
        break
    return result

class Nand:
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
    if instruction.dependency1 == 'NA':
      src1 = RF.R[instruction.source1]
    else:
      for entry in ROB.entries:
        if entry.tag == instruction.dependency1:
          src1 = entry.result
          break
    if instruction.dependency2 == 'NA':
      src2 = RF.R[instruction.source2]
    else:
      for entry in ROB.entries:
        if entry.tag == instruction.dependency2:
          src2 = entry.result
          break
    if self.cycle == 1:
        self.result = ~(src1 & src2)
    if self.busy == False:
        self.cycle = 0
        self.busy = True

  def incr_cycle(self):
    self.cycle += 1

  def khalasty(self):
    if self.cycle >= 1:
      return 'YES'
    else:
      return 'NO'

  def write(self, instruction):
    if self.cycle >= 1 and self.busy == True:
      result = self.result
    else:
      result = None
    self.busy = False
    for station in self.RS:
      if station.tag == instruction.tag:
        station.busy = False
        break
    return result

class FU:
  def __init__(self):
    self.adder = adder()
    self.multiplier = mul()
    #self.brancher = brancher()
    self.Nand = Nand()
    #self.jmp = jmp()
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
        print(instruction.immediate)
        print(self.RF.R[instruction.source1].data)
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
  
  def execute(self, instruction, ROB):
    if instruction.instType == 'ADD' or instruction.instType == 'SUB':
      self.adder.execute(instruction, self.RF, ROB)
    elif instruction.instType == 'ADDI':
      self.adder.execute(instruction, self.RF, ROB)
    elif instruction.instType == 'MUL':
      self.multiplier.execute(instruction, self.RF, ROB)
    elif instruction.instType == 'LW':
        print("FU is executing Load")
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
    if instruction == 'ADDER':
      return self.adder.RS_empty()
    elif instruction == 'MULTIPLIER':
      return self.multiplier.RS_empty()
    elif instruction == 'LOADER':
      return self.loader.RS_empty()
    elif instruction == 'STORER':
      #return 'YES'
      return self.storer.RS_empty()
    elif instruction == 'BRANCHER':
      return 'YES'
      #return self.brancher.RS_empty()
    elif instruction == 'JUMPER':
        return 'YES'
    #  return self.jmp.RS_empty()
    elif instruction == 'NANDER':
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
    for R in self.RF.R.values():
      if R.tag == tag:
        R.data = result
        break
    


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
            self.dependency1 = 'NA'
            self.dependency2 = 'NA'
            self.ready_to_write = 'NA'
            self.result = 'NA'
            self.status = 'NA'
            self.condition = 0 # Added by KA
     
     
          
#def issue(instruction, tag, FU):
#           instruction.issued = 'YES'
#           FU.issue
           
               
               
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
    label_sum=0
    label_indices =list()
    label_names = list()
    j=0
    
    inst = [None]*(len(instructions))
     
    for i in range(len(instructions)):   #parsing the instructions read
       
       inst[i]=instructions[i].split()
       instructions[i]=instruction() 
       
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
          instructions[i].source2='NA'
          instructions[i].immediate=inst[i][3]
       else:
          #print("INVALID INSTRUCTION (maybe a label?)")
         # print("line no.",i+1)
          label_sum=label_sum+1
          label_indices.append(i)
          label_names.append( instructions[i].instType)
          
        #counter to account for size changes everytime I delete  
    for i in range(len(label_indices)):
#         print('i will delete ', instructions[label_indices[i]-j].instType )
         del instructions[label_indices[i]-j]
         j+=1
         
     #mapping instruction types to responsible functional units
    for i in range(len(instructions)):
       instructions[i].tag=i   #setting the instruction order 
       if(instructions[i].instType == 'ADD' or instructions[i].instType == 'SUB' or instructions[i].instType == 'ADDI'):
           instructions[i].functional_unit = 'ADDER'
       elif(instructions[i].instType == 'JMP' or instructions[i].instType == 'JALR' or instructions[i].instType == 'RET'):
            instructions[i].functional_unit = 'JUMPER'
       elif(instructions[i].instType == 'MUL'):
           instructions[i].functional_unit= 'MULTIPLIER'
       elif(instructions[i].instType == 'NAND'):
           instructions[i].functional_unit= 'NANDER' 
       elif(instructions[i].instType == 'LW'):
           instructions[i].functional_unit= 'LOADER' 
       elif(instructions[i].instType == 'SW'):
           instructions[i].functional_unit= 'STORER'   
       elif(instructions[i].instType == 'BEQ'):
           instructions[i].functional_unit= 'BRANCHER'  
           
    sources1_list = [None]*(len(instructions))
    sources2_list = [None]*(len(instructions))
    destination_list = [None]*(len(instructions))
    #print(label_sum)   #used for testing       
    for i in range (len(instructions)):  #cleaning up
       instructions[i].source1 = instructions[i].source1.strip(',')
       instructions[i].source2 = instructions[i].source2.strip(',')
       instructions[i].destination = instructions[i].destination.strip(',')
       sources1_list[i]= instructions[i].source1 
       sources2_list[i]= instructions[i].source2 
       destination_list[i]= instructions[i].destination 
       
       
    for i in range (1,len(instructions)):  #checking possible dependencies
        for j in range(i):
            if(sources1_list[i] == destination_list[j]):
                instructions[i].dependency1=j
            if(sources2_list[i] == destination_list[j]):
                instructions[i].dependency2=j
    
         
        
         
    return [label_indices, label_names]      
           
       
       
       
       
       
       
       
       
       
       