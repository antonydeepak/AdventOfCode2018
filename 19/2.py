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
        self.all_fns = [self.addr, self.addi, self.mulr, self.muli, self.banr, \
            self.bani, self.borr, self.bori, self.setr, self.seti, self.gtir, self.gtri, self.gtrr, self.eqir, self.eqri, self.eqrr]

    def addr(self, memory, a, b, c):
        memory.registers[c].value = memory.registers[a].value + memory.registers[b].value

    def addi(self, memory, a, b, c):
        memory.registers[c].value = memory.registers[a].value + b

    def mulr(self, memory, a, b, c):
        memory.registers[c].value = memory.registers[a].value * memory.registers[b].value

    def muli(self, memory, a, b, c):
        memory.registers[c].value = memory.registers[a].value * b

    def banr(self, memory, a, b, c):
        memory.registers[c].value = memory.registers[a].value & memory.registers[b].value

    def bani(self, memory, a, b, c):
        memory.registers[c].value = memory.registers[a].value & b

    def borr(self, memory, a, b, c):
        memory.registers[c].value = memory.registers[a].value | memory.registers[b].value

    def bori(self, memory, a, b, c):
        memory.registers[c].value = memory.registers[a].value | b

    def setr(self, memory, a, b, c):
        memory.registers[c].value = memory.registers[a].value

    def seti(self, memory, a, b, c):
        memory.registers[c].value = a

    def gtir(self, memory, a, b, c):
        memory.registers[c].value = 1 if a>memory.registers[b].value else 0

    def gtri(self, memory, a, b, c):
        memory.registers[c].value = 1 if memory.registers[a].value>b else 0
        
    def gtrr(self, memory, a, b, c):
        memory.registers[c].value = 1 if memory.registers[a].value>memory.registers[b].value else 0

    def eqir(self, memory, a, b, c):
        memory.registers[c].value = 1 if a==memory.registers[b].value else 0

    def eqri(self, memory, a, b, c):
        memory.registers[c].value = 1 if memory.registers[a].value==b else 0

    def eqrr(self, memory, a, b, c):
        memory.registers[c].value = 1 if memory.registers[a].value==memory.registers[b].value else 0

    def _find(self, value, iterable, key):
        for e in iterable:
            if (key(e) == value):
                return e

    def execute(self, command, memory, a, b, c):
        fn = self._find(command, self.all_fns, lambda x: x.__name__)
        return fn(memory, a, b, c)

def get_memory(memory):
    return (list(map(lambda x: x.value, memory.registers)))

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()

    # create program
    program = []
    for line in lines[1:]:
        line = line.rstrip()
        command, *args = line.split()
        program.append((command, list(map(int, args))))

    # A simulation for register 0 with the helper program below. The helper program was determined after observing the loop in which the program spends a fortune amount of time
    # _0value = 0
    # for _1value in range(1, total):
    #     _5value = total // _1value
    #     if _5value*_1value == total:
    #         _0value += _1value
    # print(_0value)

    # The following states were determined
    # ip:9 [4401637, 10551274, 9, 10551276, 10551275, 0] ('gtrr', [3, 4, 5])
    # More advanced than previous 
    # ip:9 [14952912, 10551275, 9, 10551276, 10551275, 0] ('gtrr', [3, 4, 5])
    memory = Memory(6)
    cpu = Cpu()

    memory.registers[0].value = 14952912
    memory.registers[1].value = 10551275
    memory.registers[2].value = 9
    memory.registers[3].value = 10551276
    memory.registers[4].value = 10551275
    memory.registers[5].value = 0

    ip = memory.registers[2]

    n = len(program)
    while ip.value>=0 and ip.value<n:
        instruction = program[ip.value]
        command = instruction[0]
        args = instruction[1]
        cpu.execute(command, memory, *args)

        ip.value += 1

    print(f"{get_memory(memory)}")
    ip.value = 0