import re
import os

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

    for root, dirs, traces in os.walk(traces_path):
        for trace in traces:
            if os.path.exists(os.path.join(criterion_path, trace)):
                continue
            print(os.path.join(traces_path, trace))
            assemble = []
            t = open(os.path.join(traces_path, trace), 'r')
            lines = t.readlines()
            t.close()

            # 提取汇编指令
            for line in lines:
                instruction = str(line).split('\t')[-1]
                assemble.append(instruction)

            # 保存汇编指令
            with open(os.path.join(assemble_path, trace), 'w') as output_file:
                for instruction in assemble:
                    output_file.write(instruction.strip() + '\n')

            # 提取 criterion
            criterion = []
            for line in reversed(lines[-6:]):
                instruction = str(line).split('\t')[-1]
                criterion.append(instruction)
            
            func = (re.split(r'\s+', lines[-6].strip())[5]).split('+')[0]
            # print(func)
            for line in reversed(lines[:-6]):
                execution_trace = re.split(r'\s+', line.strip())
                instruction = str(line).split('\t')[-1]
                # print(execution_trace)
                # print(line)
                if execution_trace[5].split('+')[0] != func:
                    # print(execution_trace[5].split('+')[0])
                    break
                criterion.append(instruction)

            # 保存 criterion
            with open(os.path.join(criterion_path, trace), 'w') as output_file:
                for instruction in reversed(criterion):
                    output_file.write(instruction.strip() + '\n')


