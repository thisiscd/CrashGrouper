import re
import os
from typing import List, Set
from instruction import *

## 仅考虑以 %r 开头的寄存器的直接数据依赖
## 暂未考虑 pop push

# 用于匹配以 %r 开头的寄存器
register_pattern = re.compile(r'%r[a-zA-Z0-9]+')


def get_registers_used(slicing_criterion: List[str]) -> Set[str]:
    registers_used = set()
    # todo
    for instruction in reversed(slicing_criterion):
        found_registers = register_pattern.findall(instruction)
        registers_used.update(found_registers)
        if instruction.find('xor') != -1 or instruction.find('and') != -1:
            if len(found_registers) == 2 and found_registers[0] == found_registers[1]:
                for reg in found_registers:
                    if reg in registers_used:
                        registers_used.remove(reg) 
        elif instruction.find('mov') != -1 and len(found_registers) < 2:
            for reg in found_registers:
                if reg in registers_used:
                    registers_used.remove(reg) 
                
    return registers_used


def backwards_slicing(instructions: List[str], registers_used: Set[str]) -> List[str]:
    slice = []
    for instruction in reversed(instructions):
        found_registers = register_pattern.findall(instruction)
        for reg in found_registers:
            if reg in registers_used:
                slice.append(instruction)
                # print(instruction)
        
        if instruction.find('xor') != -1 or instruction.find('and') != -1:
            if len(found_registers) == 2 and found_registers[0] == found_registers[1]:
                for reg in found_registers:
                    if reg in registers_used:
                        registers_used.remove(reg) 
                if len(registers_used) == 0:
                    break
        elif instruction.find('mov') != -1 and  len(found_registers) < 2:
            for reg in found_registers:
                if reg in registers_used:
                    registers_used.remove(reg) 
            if len(registers_used) == 0:
                break
        
    # print(registers_used)
    return slice


def main():
    
    path = 'G:\\'

    for folder_program in os.listdir(path):
        # if folder_program != 'tcpdump':
        #     continue
        program_path = os.path.join(path, folder_program)
        assemble_path = os.path.join(program_path, 'assemble')
        criterion_path = os.path.join(program_path, 'criterion')
        slices_path = os.path.join(program_path, 'slice')
        traces_path = os.path.join(program_path, 'first_trace')

        os.makedirs(assemble_path, exist_ok=True)
        os.makedirs(criterion_path, exist_ok=True)
        os.makedirs(slices_path, exist_ok=True)
        os.makedirs(traces_path, exist_ok=True)


        for root, dirs, criterions in os.walk(criterion_path):
            for criterion in criterions:
                print(os.path.join(criterion_path, criterion))
                f = open(os.path.join(criterion_path, criterion))
                inst_cri = f.readlines()
                f.close()
                f = open(os.path.join(assemble_path, criterion))
                instructions = f.readlines()
                f.close()
                
                registers_used = get_registers_used(inst_cri)
                slice = backwards_slicing(instructions[:-len(inst_cri)], registers_used)

                with open(os.path.join(slices_path, criterion), 'w') as output_file:
                    for instr in reversed(slice):
                        output_file.write(instr + '\n')
                    for instr in inst_cri:
                        output_file.write(instr + '\n')



if __name__== "__main__" :
    main()
