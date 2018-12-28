import re
import functools
import sys

def parse(line):
    matches = re.search("position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", line)
    return [(int(matches[1]),int(matches[2])), (int(matches[3]),int(matches[4]))]

def project(point, velocity, time):
    displacement = (velocity[0]*time, velocity[1]*time)
    return (point[0]+displacement[0], point[1]+displacement[1])

def display(points, min_x, min_y, max_x, max_y):
    # print(min_x, max_x, min_y, max_y)
    for j in range(min_y, max_y+1):
        for i in range(min_x, max_x+1):
            if (i,j) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()
    points = []
    for line in lines:
        points.append(parse(line))
    
    time = 0
    INF = 1000000000000000000
    prev_spread = (INF, INF)
    prev_projections = None
    while True:
        projections = set()
        for point in points:
            p,v = point
            projections.add(project(p, v, time))
        # print(projections)

        # compute minimals
        min_x = min(projections, key=lambda x: x[0])[0]
        min_y = min(projections, key=lambda x: x[1])[1]
        max_x = max(projections, key=lambda x: x[0])[0]
        max_y = max(projections, key=lambda x: x[1])[1]

        #measures cohesiveness
        spread = (max_x-min_x, max_y-min_y)
        if spread>prev_spread:
            display(prev_projections, min_x, min_y, max_x, max_y)
            print(f"seconds: {time-1}")
            sys.exit(0)
        prev_spread = spread
        prev_projections = projections

        time += 1

