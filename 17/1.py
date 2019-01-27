'''
After thinking for a long time, I think the best way is to do a DFS approach exploring the flow of water.
Atleast the major states of the system should be captured - clay, sand & moving water. 
We can start from the source and explore every node
Every node has three actions is has to take- go down, go left, go right.
    You can go down only when there is sand
    You can go left only if the left node has clay or still water down
    You can only go right if the right node has a clay or still water down
    When you are bounded on left or right you can mark the side you are bounded.
        This can get cascaded and finally the parent that has both left and right marked can mark that entire span to be bounded. This makes a still water
'''

import operator
import sys
import re

sys.setrecursionlimit(10000)

class AreaType(object):
    Clay,Sand,StillWater,MovingWater = 0,1,2,3

def parse(line):
    matches = re.search("(\w)=(\d+), (\w)=(\d+)..(\d+)", line)
    return {matches[1]: (int(matches[2]),int(matches[2])), matches[3]: (int(matches[4]),int(matches[5]))}

def down(point):
    return tuple(map(operator.add, point, [0,1]))

def left(point):
    return tuple(map(operator.add, point, [-1,0]))

def right(point):
    return tuple(map(operator.add, point, [1,0]))

def get_area_type(point):
    return region[point] if point in region else AreaType.Sand

def fill_internal(point, min_y, max_y):
    # down
    d = down(point)
    if (min_y <= d[1] <= max_y) and get_area_type(d) == AreaType.Sand:
        region[d] = AreaType.MovingWater
        fill_internal(d, min_y, max_y)

    # left
    l = left(point)
    left_bound = None
    if (get_area_type(d) == AreaType.StillWater or get_area_type(d) == AreaType.Clay):
        if (get_area_type(l) == AreaType.Sand):
            region[l] = AreaType.MovingWater
            left_bound = fill_internal(l, min_y, max_y)
        elif (get_area_type(l) == AreaType.Clay):
            left_bound = l[0]
    
    # right
    r = right(point)
    right_bound = None
    if (get_area_type(d) == AreaType.StillWater or get_area_type(d) == AreaType.Clay):
        if (get_area_type(r) == AreaType.Sand):
            region[r] = AreaType.MovingWater
            right_bound = fill_internal(r, min_y, max_y)
        elif (get_area_type(r) == AreaType.Clay):
            right_bound = r[0]
    
    if left_bound and right_bound:
        for i in range(left_bound, right_bound):
            if region[(i,point[1])] == AreaType.MovingWater:
                region[(i,point[1])] = AreaType.StillWater
        return None

    return left_bound if left_bound else right_bound

def fill(region):
    min_y = min(region.keys(), key=lambda p: p[1])[1]
    max_y = max(region.keys(), key=lambda p: p[1])[1]
    starting = (500,min_y)
    region[starting] = AreaType.MovingWater
    fill_internal(starting, min_y, max_y)

if __name__ == '__main__':
    # file_name = "./17/test.in"
    file_name = "./17/1.in"
    lines = open(file_name, 'r').readlines()
    region = {}

    for line in lines:
        area = parse(line)
        for j in range(area['y'][0], area['y'][1]+1):
            for i in range(area['x'][0], area['x'][1]+1):
                region[(i,j)] = AreaType.Clay
    
    fill(region)
    result = list(filter(lambda x: region[x] == AreaType.StillWater or region[x] == AreaType.MovingWater, region))
    print(len(result))
