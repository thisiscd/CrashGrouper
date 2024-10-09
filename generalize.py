import re
import os

def generalize_assembly(slice):
    generalized = []
    for line in slice:
        # 替换立即数
        if line == '\n':
            continue
        line = re.sub(r'\%[a-z]{1,3}(?:[0-9]+|[a-z]{1,3})*', 'REG', line)
        line = re.sub(r'\-?0[xX][0-9a-fA-F]+', 'IMM', line)
        generalized.append(line)
    return generalized

path = 'G:\\'

for folder_program in os.listdir(path):
    # if folder_program != 'tcpdump':
    #     continue
    program_path = os.path.join(path, folder_program)
    assemble_path = os.path.join(program_path, 'assemble')
    criterion_path = os.path.join(program_path, 'criterion')
    slices_path = os.path.join(program_path, 'slice')
    traces_path = os.path.join(program_path, 'first_trace')
    generalize_path = os.path.join(program_path, 'generalized')

    os.makedirs(assemble_path, exist_ok=True)
    os.makedirs(criterion_path, exist_ok=True)
    os.makedirs(slices_path, exist_ok=True)
    os.makedirs(traces_path, exist_ok=True)
    os.makedirs(generalize_path, exist_ok=True)


    for root, dirs, slices in os.walk(slices_path):
        for slice in slices:
            print(os.path.join(slices_path, slice))
            f = open(os.path.join(slices_path, slice))
            sli = f.readlines()
            f.close()

            generalized = generalize_assembly(sli)
            
            with open(os.path.join(generalize_path, slice), 'w') as output_file:
                for instr in generalized:
                    output_file.write(instr + '\n')