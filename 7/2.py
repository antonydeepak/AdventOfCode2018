import re
from collections import deque
from heapq import heapify
from heapq import heappush
from heapq import heappop

def parse(line):
    matches = re.search("Step (\w) must be finished before step (\w) can begin.", line)
    return (matches[1], matches[2])

base = 60
def cost(item):
    return base + ord(item) - ord('A') + 1

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').read().splitlines()
    G = {}
    for line in lines:
        u,v = parse(line)
        if v not in G:
            G[v] = []
        if u not in G:
            G[u] = []
        G[u].append(v)

    # Kahn's algorithm
    incident_edges = {}
    for u in G:
        if u not in incident_edges:
            incident_edges[u] = 0
        for v in G[u]:
            if v not in incident_edges:
                incident_edges[v] = 0
            incident_edges[v] += 1

    frontier = []
    max_queue = 5
    for u,count in incident_edges.items():
        if count == 0:
            frontier.append([cost(u),u])
    frontier,reserve = frontier[0:max_queue],frontier[max_queue:]
    heapify(frontier)
    heapify(reserve)

    time = 0
    while len(frontier) > 0:
        # print(time, frontier)
        c,u = heappop(frontier)
        time += c
        for step in frontier:
            step[0] -= c
        while len(frontier)<max_queue and len(reserve)>0:
            heappush(frontier, heappop(reserve))

        for v in G[u]:
            assert(incident_edges[v] > 0)
            incident_edges[v] -= 1
            if incident_edges[v] == 0:
                if len(frontier)<max_queue:
                    heappush(frontier, [cost(v),v])
                else:
                    heappush(reserve, [cost(v),v])

    for u,count in incident_edges.items():
        assert(count == 0)
    print(time)