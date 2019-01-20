import re

def parse(line):
    matches = re.search("pos=<([-+]?\d+),([-+]?\d+),([-+]?\d+)>, r=([-+]?\d+)", line)
    return (int(matches[1]), int(matches[2]), int(matches[3])), int(matches[4])

def manhattan_distance(a, b):
    x1,y1,z1 = a
    x2,y2,z2 = b
    return abs(x1-x2)+abs(y1-y2)+abs(z1-z2)

if __name__ == '__main__':
    # file_name = "./23/test.in"
    file_name = "./23/1.in"
    lines = open(file_name, 'r').readlines()
    bots = []
    for line in lines:
        coord,signal = parse(line.rstrip())
        bots.append((coord, signal))
    bots = sorted(bots, key=lambda x: x[1], reverse=True) #strength
    best_coord = bots[0][0]
    best_signal = bots[0][1]
    count = 0
    for bot in bots:
        coord = bot[0]
        signal = bot[1]
        count += 1 if manhattan_distance(best_coord, coord) <= best_signal else 0
    print(count)
