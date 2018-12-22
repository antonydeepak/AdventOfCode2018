import re
from collections import deque
from heapq import heapify
from heapq import heappush
from heapq import heappop

def parse(line):
    matches = re.search("Step (\w) must be finished before step (\w) can begin.", line)
    return (matches[1], matches[2])

if __name__ == '__main__':
    #file_name = "test.in"
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
    for u,count in incident_edges.items():
        if count == 0:
            frontier.append(u)
    heapify(frontier)

    steps = []
    while len(frontier) > 0:
        u = heappop(frontier)
        steps.append(u)
        for v in G[u]:
            assert(incident_edges[v] > 0)
            incident_edges[v] -= 1
            if incident_edges[v] == 0:
                heappush(frontier, v)
    for u,count in incident_edges.items():
        assert(count == 0)
    print(''.join(steps))