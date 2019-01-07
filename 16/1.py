# Problem is about finding samples that match 3 or more opcodes 
# For each sample
#   Enumerate thru all the opcode implementations by passing it the notion of a "register"
#   Check the register value "C" after execution and see if that matches the expected output
#   If match, then increment that there is an opcode match

import re

class Register(object):
    def __init__(self):
        self.value = 0

class Memory(object):
    def __init__(self, capacity):
        self.registers = []
        for _  in range(capacity):
            self.registers.append(Register())

class Cpu(object):
    def __init__(self):
        self.all_opcodes = [self.addr, self.addi, self.mulr, self.muli, self.banr, \
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

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()
    n = len(lines)
    i = 0
    memory = Memory(4)
    cpu = Cpu()
    total_samples_gt_3 = 0
    while i<n:
        before = parse_before(lines[i].rstrip())
        i += 1
        instruction = list(map(int, lines[i].rstrip().split()))
        i += 1
        after = parse_after(lines[i].rstrip())
        i += 1

        total_opcode_match = 0
        for opcode in cpu.all_opcodes:
            for j,value in enumerate(before):
                memory.registers[j] = value

            opcode(memory, *instruction[1:])

            score = 0
            for j,value in enumerate(after):
                score += 1 if memory.registers[j] == value else 0
            total_opcode_match += 1 if (score == len(after)) else 0
        total_samples_gt_3 += 1 if total_opcode_match>=3 else 0

        i += 1
    print(total_samples_gt_3)