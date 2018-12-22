import re

def parse(line):
    matches = re.search("(\d+), (\d+)", line)
    return (int(matches[1]), int(matches[2]))

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

if __name__ == '__main__':
    #file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').read().splitlines()
    points = list(map(parse, lines))
    sort_x = list(sorted(points, key=lambda x: x[0]))
    sort_y = list(sorted(points, key=lambda x: x[1]))
    min_x = sort_x[0][0]
    max_x = sort_x[-1][0]
    min_y = sort_y[0][1]
    max_y = sort_y[-1][1]

    #print(min_x, max_x, min_y, max_y)
    
    region_s = 0
    limit = 10000
    #limit = 32
    for i in range(max_x):
        for j in range(max_y):
            total_d = 0
            for point in points:
                total_d += distance((i,j), point)
            if total_d<limit:
            #if total_d<32:
                region_s += 1
    
    print(region_s)