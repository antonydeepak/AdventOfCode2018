# Problem is about finding samples that match 3 or more opcodes 
# For each sample
#   Enumerate thru all the opcode implementations by passing it the notion of a "register"
#   Check the register value "C" after execution and see if that matches the expected output
#   If match, then increment that there is an opcode match

import re
from functools import reduce

class Memory(object):
    def __init__(self, capacity):
        self.registers = [0] * capacity

class Cpu(object):
    def __init__(self):
        self.all_fns = [self.addr, self.addi, self.mulr, self.muli, self.banr, \
            self.bani, self.borr, self.bori, self.setr, self.seti, self.gtir, self.gtri, self.gtrr, self.eqir, self.eqri, self.eqrr]

    def addr(self, memory, a, b, c):
        memory.registers[c] = memory.registers[a] + memory.registers[b]

    def addi(self, memory, a, b, c):
        memory.registers[c] = memory.registers[a] + b

    def mulr(self, memory, a, b, c):
        memory.registers[c] = memory.registers[a] * memory.registers[b]

    def muli(self, memory, a, b, c):
        memory.registers[c] = memory.registers[a] * b

    def banr(self, memory, a, b, c):
        memory.registers[c] = memory.registers[a] & memory.registers[b]

    def bani(self, memory, a, b, c):
        memory.registers[c] = memory.registers[a] & b

    def borr(self, memory, a, b, c):
        memory.registers[c] = memory.registers[a] | memory.registers[b]

    def bori(self, memory, a, b, c):
        memory.registers[c] = memory.registers[a] | b

    def setr(self, memory, a, b, c):
        memory.registers[c] = memory.registers[a]

    def seti(self, memory, a, b, c):
        memory.registers[c] = a

    def gtir(self, memory, a, b, c):
        memory.registers[c] = 1 if a>memory.registers[b] else 0

    def gtri(self, memory, a, b, c):
        memory.registers[c] = 1 if memory.registers[a]>b else 0
        
    def gtrr(self, memory, a, b, c):
        memory.registers[c] = 1 if memory.registers[a]>memory.registers[b] else 0

    def eqir(self, memory, a, b, c):
        memory.registers[c] = 1 if a==memory.registers[b] else 0

    def eqri(self, memory, a, b, c):
        memory.registers[c] = 1 if memory.registers[a]==b else 0

    def eqrr(self, memory, a, b, c):
        memory.registers[c] = 1 if memory.registers[a]==memory.registers[b] else 0

def parse_before(line):
    matches = re.search("Before: \[([0123]), ([0123]), ([0123]), ([0123])\]", line)
    values = [matches[1], matches[2], matches[3], matches[4]]
    return [int(v) for v in values]

def parse_after(line):
    matches = re.search("After:  \[([0123]), ([0123]), ([0123]), ([0123])\]", line)
    values = [matches[1], matches[2], matches[3], matches[4]]
    return [int(v) for v in values]

def converge(opcode_fn_map, opcode, used_fns):
    # base case; all opcodes satisfied
    if opcode >= len(opcode_fn_map):
        return (True, {})

    for fn in opcode_fn_map[opcode]:
       if fn not in used_fns:
           used_fns.add(fn)
           result,state = converge(opcode_fn_map, opcode+1, used_fns)
           if result:
               state[opcode] = fn
               return (True, state)
           used_fns.remove(fn)

    return (False, None)

def find(value, iterable, key):
    for e in iterable:
        if (key(e) == value):
            return e

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()
    n = len(lines)

    opcode_fn_map = {}
    for i in range(16):
        opcode_fn_map[i] = []

    # explore possibilities for opcode
    i = 0
    memory = Memory(4)
    cpu = Cpu()
    while i<n:
        before = parse_before(lines[i].rstrip())
        i += 1
        instruction = list(map(int, lines[i].rstrip().split()))
        opcode = instruction[0]
        i += 1
        after = parse_after(lines[i].rstrip())
        i += 1

        opcode_fn_map[opcode].append(set())
        for fn in cpu.all_fns:
            for j,value in enumerate(before):
                memory.registers[j] = value

            fn(memory, *instruction[1:])

            score = 0
            for j,value in enumerate(after):
                score += 1 if memory.registers[j] == value else 0
            if (score == len(after)):
                opcode_fn_map[opcode][-1].add(fn.__name__)

        i += 1

    # reduce possibilities
    for opcode in opcode_fn_map:
        opcode_fn_map[opcode] = reduce(lambda x,y: x.intersection(y), opcode_fn_map[opcode])

    # converge to one possibility
    _,opcode_fn_map = converge(opcode_fn_map, 0, set())

    # test program
    test_program_input = "2.in"
    lines = open(test_program_input, 'r').readlines()
    memory = Memory(4)
    cpu = Cpu()
    for line in lines:
        instruction = list(map(int, line.rstrip().split()))
        opcode = instruction[0]
        fn = find(opcode_fn_map[opcode], cpu.all_fns, lambda x: x.__name__)
        fn(memory, *instruction[1:])
    print(memory.registers[0])