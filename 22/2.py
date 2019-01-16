import heapq
import operator
import re

class RegionType(object):
    Rock,Wet,Narrow = 0,1,2

class Tool(object):
    Torch,Climber,Neither = 0,1,2

def get_type(position, erosion_level):
    return erosion_level[position] % 3

def parse_depth(line):
    matches = re.search("depth: (\d+)", line)
    return matches[1]

def parse_target(line):
    matches = re.search("target: (\d+),(\d+)", line)
    return (matches[1],matches[2])

def shortest_path_djikstra(source, target, erosion_level):
    # helper methods
    INF = 10000000000
    distance = {}
    visited_edges = set()
    supported_equipments = {
        RegionType.Rock : [Tool.Climber, Tool.Torch],
        RegionType.Wet : [Tool.Climber, Tool.Neither],
        RegionType.Narrow : [Tool.Torch, Tool.Neither]
    }
    total_explored_edges_to_target = 0 #we exit when we have explored all 4 edges to reach the target
    best_equipments = {}

    def relax(u, v):
        nonlocal total_explored_edges_to_target

        to_type = get_type(v, erosion_level)
        equipments = best_equipments[u]
        usable_equipments = set([equipment for equipment in equipments if can_use_equipment(equipment, to_type)])
        cost = 1 if len(usable_equipments)>0 else 8 # None of the equipments can be used and hence have to eat the cost of 
        usable_equipments = usable_equipments if len(usable_equipments)>0 else set(supported_equipments[to_type]) #swap to one of the supported equipment type

        if v == target or u == target:
            total_explored_edges_to_target += 1
        if get_distance(u)+cost == get_distance(v):
            best_equipments[v] = best_equipments[v].union(usable_equipments)
        elif get_distance(u)+cost < get_distance(v):
            best_equipments[v] = usable_equipments.copy()
            distance[v] = distance[u]+cost
            return (True, distance[v])

        return (False, None)

    def can_use_equipment(equipment, region_type):
        return equipment in supported_equipments[region_type]
        
    def get_distance(u):
        return distance[u] if u in distance else INF

    directions = [(0,-1), (0,1), (1,0), (-1,0)] #N,S,E,W
    def get_adjacents(u):
        for direction in directions:
            v = tuple(map(operator.add, u, direction))
            if (v[0]>=0 and v[1]>=0):
                yield v

    # Djikstra
    distance[source] = 0
    best_equipments[source] = set([Tool.Torch])
    pq = [(distance[source], source)]
    while total_explored_edges_to_target < 4:
        d,u = heapq.heappop(pq)
        
        if d > get_distance(u): # lazy deletion because we already found a shorter path to that node
            continue

        for v in get_adjacents(u):
            if not ((u,v) in visited_edges or (v,u) in visited_edges):
                visited_edges.add((u,v))
                relaxed,cost = relax(u, v)
                if relaxed:
                    heapq.heappush(pq, (cost, v))

    return distance[target] + (0 if Tool.Torch in best_equipments[target] else 7)

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()
    depth = int(parse_depth(lines[0]))
    target = tuple(map(int, parse_target(lines[1])))
    start = (0,0)

    additional_coverage = 700#Since the terrain can extend beyond problem 1 this is just a approximation
    geo_index = {}
    erosion_level = {}
    for i in range(start[1], target[1]+additional_coverage):#y
        for j in range(start[0], target[0]+additional_coverage): #X
            if (i==0 and j==0) or (i==target[1] and j==target[0]):
                geo_index[(j,i)] = 0
            elif (i == 0):
                geo_index[(j,i)] = j*16807
            elif (j == 0):
                geo_index[(j,i)] = i*48271
            else:
                geo_index[(j,i)] = erosion_level[(j-1,i)] * erosion_level[(j,i-1)]
            erosion_level[(j,i)] = (geo_index[(j,i)] + depth) % 20183

    print(shortest_path_djikstra(start, target, erosion_level))