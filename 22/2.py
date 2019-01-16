import re
import 

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
    INF = 10000000000
    distance = {}
    visited_edges = set()
    supported_equipments = {
        RegionType.Rock : [Tool.Climber, Tool.Torch],
        RegionType.Wet : [Tool.Climber, Tool.Neither],
        RegionType.Narrow : [Tool.Torch, Tool.Neither]
    }
    
    # continue writing djikstra
    # Have to pass equipment as well in the pq
    # When switching elements we have to queue 2 alternatives. This might question the logic behind total_explored_edges_to_target
    pq = [(0,source)]
    total_explored_edges_to_target = 0 #we exit when we have explored all 4 edges to reach the target
    while total_explored_edges_to_target < 4:
        d,u = heapq.heappop(pq)
        if d > get_distance(u): #lazy deletion because we already found a shorter path to that node
            continue
        if u == target:
            total_explored_edges_to_target += 1

        for v in get_adjacents(u):
            is_relaxed,weight = relax(u, v)
            if is_relaxed:
                heapq.heappush(weight)
    
    def relax(u, v):
        uw,un = u
        vw,vn = v

        if distance[un]+uw < distance[vn]:
            distance[vn] = distance[un]+w
            return (True, (distance[vn],vn))

        return (False, None)
    
    def get_cost(u, current_equipment, v):
       from_type = get_type(u, erosion_level)
       to_type = get_type(v, erosion_level)
       return 1 if can_use_equipment(to_type, equipment) else 7
    
    def can_use_equipment(region_type, equipment):
        return equipment in supported_equipments[region_type]
        
    def get_distance(u):
        return distance[u] if u in distance else INF
    
    directions = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)} #N,S,E,W
    def get_adjacents(u):
        for direction in directions:
            v = tuple(map(operator.add, u, direction))
            if (v[0]>=0 and v[1]>=0):
                yield v

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

    # Run a Djikstra start to target until you have seen the shortest path for all possible edges of the target
    # Just make sure to store the edges so that each edge is explored only once since this is undirected graph

    visited_edges = set()
