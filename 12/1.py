import re

def parse_state(line):
    return re.search("initial state: (.*)", line)[1]

def parse_spread(line):
    matches = re.search("([.#]{5}) => ([.#])", line)
    return matches[1],matches[2]

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()
    initial_state = parse_state(lines[0])
    spread_patterns = {}
    for i in range(2, len(lines)):
        pattern,spread = parse_spread(lines[i])
        spread_patterns[pattern] = spread

    pots_with_plant = set()
    for i in range(len(initial_state)):
        if initial_state[i] == '#':
            pots_with_plant.add(i)

    # generations = 20
    generations = 50000000000
    for _ in range(generations):
        new_pots_with_plant = set()
        for pot_id in pots_with_plant:
            # find patterns where i is the index of the pot_id
            for i in range(5):
                pattern = ['.']*5
                pattern[i] = '#'
                for j in range(0, i):
                    pattern[j] = '#' if ((pot_id-i+j) in pots_with_plant) else '.'
                for j in range(i+1, 5):
                    pattern[j] = '#' if ((pot_id-i+j) in pots_with_plant) else '.'
                pattern = ''.join(pattern)
                if (pattern in spread_patterns) and spread_patterns[pattern] == '#':
                    new_pot_with_plant_index = pot_id-i+2
                    if new_pot_with_plant_index not in new_pots_with_plant:
                        new_pots_with_plant.add(new_pot_with_plant_index)
        pots_with_plant = new_pots_with_plant

    print(sum(pots_with_plant))