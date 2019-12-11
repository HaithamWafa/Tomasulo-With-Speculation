# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 11:24:17 2019

@author: Haitham Samir
"""




from processor import *

ROB=ROB(8)
F=FU()

issued_inst = list()
exec_inst = list()
write_inst = list()
commit_inst = list()
def execute(instructions):
    instructions.status='exec'
    exec_inst.append(instructions.tag)
    print('in execute funct',issued_inst)
    #issued_inst.remove(instructions.tag)
    
    
def issue(instructions):
    instructions.status = 'issued'
    #print('inside issue function', instructions.tag)
    issued_inst.append(instructions.tag)
    F.issue(instructions)

    
    
def main():
   
   Global_Clk=0
    
   instructions = Import_Instruction_File() #imports instructions as a list of strings
   labels= Parse_Instructions(instructions)  #labels is a list of 2 lists, labels[0][0] first []: 0 for index, 1 for name
   #print(labels)
  
       

           
    #please make sure that all the following Functional units are implemented as a class and that all have a member function ".issue()"       
#   ADDER = Adder() 
#   MULTIPLIER = Multiplier()
#   LOADER = Loader()
#   STORER = Storer()
#   BRANCHER = Brancher()
#   JUMPER = Jumper()
#   NANDER = Nander()
   
      
#   for i in range(len(instructions)):
#       if(ROB.empty_entries >=2):  #this should check for the number of available entries in ROB bta3ak ya MOSTAFA
#           for j+instruction[i].tag in range(1):
#               jm=j+instruction[i].tag
#               if(instructions[jm].functional_unit== 'ADDER'):
#                   issue(instructions[jm],jm, ADDER)
#           i += 2
#       elif(ROB.empty_entries == 1):
#           for j+instruction[i].tag in range(1):
#               jm=j+instruction[i].tag
#               if(instructions[jm].functional_unit== 'ADDER'):
#                   issue(instructions[jm],jm, ADDER)
#       else:
            
           
           
            
       
   #TOMASULO CODE FLOW
   
  # print(instructions[6].functional_unit)   #used for testing  
  
   
 #  issue_cycles=0
   #issuing loop
#   for i in range(len(instructions)-1):
#       if(instructions[i].functional_unit.reservation_station.busy == 'NO' and instructions[i+1].functional_unit.reservation_station.busy and ROB.available_entries == 2):
#           instructions[i].issued = 'YES'
#           instructions[i+1].issued = 'YES'
#           issue_cycles=issue_cycles+1

#   R = ROB(16)
#   R.write(instructions[1].destination, 1)
#   R.CompleteInst(33, 1)
#   #R.commit()
#   R.print_all_entries()
#   for i in range(len(instructions)):   #testing dependcies
#       print(instructions[i].dependency1,instructions[i].dependency2)  
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   PC=0
   
   instruction_counter_for_ECALL=0
   
   
   #RF=RegFile()
   while(1):
       current_instruction_tags=list()
       #issuing
       print(ROB.empty_entries())
#       print(F.check_relevent_RS(instructions[PC].functional_unit))
       if(PC<len(instructions)):
           if(ROB.empty_entries() == 'YES' and F.check_relevent_RS(instructions[PC].functional_unit) == 'YES'):
               print(PC)
               issue(instructions[PC])
               ROB.write(instructions[PC], instructions[PC].tag)
               
              # print('heyyyyyyyyyyyyyyyyyyyyyyy',instructions[PC].status)
                #F.write(instructions[PC])
               current_instruction_tags.append(instructions[PC].tag)
               if(ROB.empty_entries() == 'YES' and F.check_relevent_RS(instructions[PC+1].functional_unit) == 'YES'):
                   issue(instructions[PC+1])
                   ROB.write(instructions[PC+1], instructions[PC+1].tag)
                   #F.write(instructions[PC+1])
                   current_instruction_tags.append(instructions[PC+1].tag)
                   PC+=1
           PC+=1
           
               
       #execution
       for i in range(len(issued_inst)):
           if(instructions[issued_inst[i]].status == 'issued' and instructions[issued_inst[i]].condition>0):
               
               #print('tag in issues',issued_inst[i])
               #print('ahoooo :', instructions[issued_inst[i]].dependency1)
               print('type', instructions[issued_inst[i]].instType)
               print('status', instructions[issued_inst[i]].status)
               print('dep1', instructions[issued_inst[i]].dependency1)
               print('dep2', instructions[issued_inst[i]].dependency2)
               #print('pc aho -->', PC)
               #print('this is 5allasty -->', F.khalasty(instructions[issued_inst[0]]))
               if(instructions[issued_inst[i]].dependency1 == 'NA'and instructions[issued_inst[i]].dependency2 == 'NA'):
                   #print('I am in the execution loop yaaaaaay')
                   execute(instructions[issued_inst[i]])
                   F.execute(instructions[issued_inst[i]], ROB)
                   #instructions[issued_inst[i]].ready_to_write=F.khalasty(instructions[issued_inst[i]])
                   #instructions[issued_inst[i]].result=F.result(instructions[issued_inst[i]])
                   #break
                   
               
               elif(instructions[issued_inst[i]].dependency1 == 'NA'):
                   if(instructions[instructions[issued_inst[i]].dependency2].status == 'written' or instructions[instructions[issued_inst[i]].dependency2].status == 'committed' ):
                       execute(instructions[issued_inst[i]])
                       F.execute(instructions[issued_inst[i]], ROB)
                  #     instructions[issued_inst[i]].ready_to_write=F.khalasty(instructions[issued_inst[i]])
                     #  instructions[issued_inst[i]].result=F.result(instructions[issued_inst[i]])
                       #break
                       
               elif(instructions[issued_inst[i]].dependency2 == 'NA'):
                   if(instructions[instructions[issued_inst[i]].dependency1].status == 'written' or instructions[instructions[issued_inst[i]].dependency1].status == 'committed' ):
                       execute(instructions[issued_inst[i]])
                       F.execute(instructions[issued_inst[i]], ROB)
                 #      instructions[issued_inst[i]].ready_to_write=F.khalasty(instructions[issued_inst[i]])
                    #   instructions[issued_inst[i]].result=F.result(instructions[issued_inst[i]])
                       #break
                
                
               elif((instructions[instructions[issued_inst[i]].dependency1].status == 'written' or instructions[instructions[issued_inst[i]].dependency1].status == 'committed') and
                  (instructions[instructions[issued_inst[i]].dependency2].status == 'written' or instructions[instructions[issued_inst[i]].dependency2].status == 'committed' )):
                   execute(instructions[issued_inst[i]])
                   F.execute(instructions[issued_inst[i]], ROB)
                #   instructions[issued_inst[i]].ready_to_write=F.khalasty(instructions[issued_inst[i]])
                   #instructions[issued_inst[i]].result=F.result(instructions[issued_inst[i]])
                   #break
                   
                   
              # else:
        #           #no execute
                   
               
       #print('this is spartaa', instructions[14].tag)        
       #writing
       for i in range(len(exec_inst)):
           print('instruction_condition', instructions[exec_inst[i]].condition)
           if(instructions[exec_inst[i]].status == 'exec'):

                instructions[exec_inst[i]].ready_to_write=F.khalasty(instructions[exec_inst[i]])
                instructions[exec_inst[i]].result=F.result(instructions[exec_inst[i]])       
                print('instruction result',i, instructions[exec_inst[i]].result)
                if(instructions[exec_inst[i]].ready_to_write == 'YES'):
                    ROB.CompleteInst(instructions[exec_inst[i]].result, instructions[exec_inst[i]].tag)
                    instructions[exec_inst[i]].status='written'
                    write_inst.append(instructions[exec_inst[i]].tag)
                    #Global_Clk +=1
                    break
       ROB.print_all_entries()   
       print(Global_Clk, current_instruction_tags, [i.status for i in instructions])
       
 
       #commit
       for i in range(len(write_inst)):
           if(instructions[write_inst[i]].status == 'written' and instructions[write_inst[i]].condition>3):
               commit_tag = ROB.commit()
               print('This is the commited tag -->', commit_tag)
               if(commit_tag != None):
                   instructions[commit_tag].status='committed'
                   F.commit(instructions[commit_tag].result,commit_tag)
                   commit_inst.append(instructions[commit_tag].tag)
           #ROB.commit()
       for i in range(len(instructions)):
           for j in range(len(issued_inst)):
               if(instructions[i].tag == instructions[issued_inst[j]].tag):
                   instructions[i].condition+=1
           for m in range(len(write_inst)):
                   if(instructions[i].tag == instructions[write_inst[m]].tag):
                       instructions[i].condition +=1
        
           
       print(Global_Clk, current_instruction_tags, [i.status for i in instructions])
      # print()
       Global_Clk+=1
       
           
       F.IncrClk()
       #instruction_counter_for_ECALL+=1
       if(Global_Clk==20):
           break
  # for i in range(len(instructions)):
   #    print(instructions[i].instType, instructions[i].tag)
   
   #print('my printt', instructions[5].instType)
   #for i in range(len(issued_inst)):
    #   print(issued_inst[i], instructions[issued_inst[i]].instType,  instructions[issued_inst[i]].tag)

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    