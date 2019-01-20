import re

def manhattan_distance(a, b):
    x1,y1,z1,k1 = a
    x2,y2,z2,k2 = b
    return abs(x1-x2)+abs(y1-y2)+abs(z1-z2)+abs(k1-k2)

def parent(i, parents):
    while parents[i] != i:
        i = parents[i]
    return i

def union(i, j, parents):
    pi = parent(i, parents)
    pj = parent(j, parents)

    if pi<pj:
        parents[pj] = pi
    elif pi>pj:
        parents[pi] = pj

def parse(line):
    return tuple(map(int, re.findall(r"(-?\d+)", line)))

if __name__ == "__main__":
    # file_name = "./25/test.in"
    file_name = "./25/1.in"
    lines = open(file_name, 'r').readlines()
    points = [parse(line.rstrip()) for line in lines]
    n = len(points)
    parents = list(range(n))

    for i in range(n):
        for j in range(i+1, n):
            if manhattan_distance(points[i], points[j]) <= 3:
                union(i, j, parents)
    
    constellation = set()
    for i in range(n):
        constellation.add(parent(i, parents))

    print(len(constellation))
