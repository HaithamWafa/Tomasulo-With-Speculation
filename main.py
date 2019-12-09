# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 11:24:17 2019

@author: Haitham Samir
"""
from processor import *

def main():
    
   instructions = Import_Instruction_File() #imports instructions as a list of strings
   Parse_Instructions(instructions)
   
   #TOMASULO CODE FLOW
   
  # print(instructions[1].destination)   #used for testing  
   
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

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    