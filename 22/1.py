import re

class RegionType(object):
    Rock,Wet,Narrow = 0,1,2

def get_type(position, erosion_level):
    return erosion_level[position] % 3

def parse_depth(line):
    matches = re.search("depth: (\d+)", line)
    return matches[1]

def parse_target(line):
    matches = re.search("target: (\d+),(\d+)", line)
    return (matches[1],matches[2])

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()
    depth = int(parse_depth(lines[0]))
    target = tuple(map(int, parse_target(lines[1])))
    start = (0,0)

    geo_index = {}
    erosion_level = {}
    for i in range(start[1], target[1]+1):#y
        for j in range(start[0], target[0]+1): #X
            if (i==0 and j==0) or (i==target[1] and j==target[0]):
                geo_index[(j,i)] = 0
            elif (i == 0):
                geo_index[(j,i)] = j*16807
            elif (j == 0):
                geo_index[(j,i)] = i*48271
            else:
                geo_index[(j,i)] = erosion_level[(j-1,i)] * erosion_level[(j,i-1)]
            erosion_level[(j,i)] = (geo_index[(j,i)] + depth) % 20183

    # risk
    print(sum((get_type(key, erosion_level) for key in erosion_level)))