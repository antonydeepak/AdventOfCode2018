# This program is same as 19.py with minor modifications in 
# Run this in pypy or a faster python interpreter than cpython as it is very slow in cpython

import os
import sys
import re

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.join(base_path, "19"))
sys.path.append(base_path)

from importlib import import_module
mod = __import__("19.1", fromlist="*")

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()

    memory = mod.Memory(6)
    cpu = mod.Cpu()

    # create program
    program = []
    for line in lines[1:]:
        line = line.rstrip()
        command, *args = line.split()
        program.append((command, list(map(int, args))))

    # init ip
    matches = re.search("#ip ([012345])", lines[0].rstrip()).groups()
    ip = memory.registers[int(matches[0])]

    n = len(program)
    repeats = set()
    last_repeat = -1
    while ip.value>=0 and ip.value<n:
        instruction = program[ip.value]
        command = instruction[0]
        args = instruction[1]
        cpu.execute(command, memory, *args)

        if command == 'eqrr':
            # check register 3
            v = memory.registers[3].value
            if v in repeats:
                break
            repeats.add(v)
            last_repeat = v

        ip.value += 1

    ip.value = 0
    print(last_repeat)