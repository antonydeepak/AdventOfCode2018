class Acre(object):
    Ground,Tree,Lumberyard = '.','|','#'

adjacents = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
def scan_adjacents(i, j, m, n, state):
    topography = {Acre.Ground: 0, Acre.Tree: 0, Acre.Lumberyard: 0}
    for v in adjacents:
        dx,dy = v
        adj = (i+dx,j+dy)
        if (adj[0]<n and adj[0]>=0 and adj[1]<m and adj[1]>=0):
            topography[state[adj]] += 1
    return topography

def scan_topography(m, n, state):
    topography = {Acre.Ground: 0, Acre.Tree: 0, Acre.Lumberyard: 0}
    for i in range(n):
        for j in range(m):
            topography[state[(i,j)]] += 1
    return topography

def next_state(i, j, m, n, state):
    current = state[(i,j)]
    adjacents = scan_adjacents(i, j, m, n, state)
    ground_tree = lambda : Acre.Tree if (current == Acre.Ground and adjacents[Acre.Tree] >= 3) else current
    tree_lumberyard = lambda : Acre.Lumberyard if (current == Acre.Tree and adjacents[Acre.Lumberyard] >= 3) else current
    stay_lumberyard = lambda : (Acre.Lumberyard if adjacents[Acre.Lumberyard] >= 1 and adjacents[Acre.Tree] >= 1 else Acre.Ground) if (current == Acre.Lumberyard) else current

    if current == Acre.Ground:
        return ground_tree()
    if current == Acre.Tree:
        return tree_lumberyard()
    if current == Acre.Lumberyard:
        return stay_lumberyard()

    raise "Invalid state"

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()

    n = len(lines) #rows
    m = len(lines[0].rstrip()) #cols

    state = {}
    for i in range(n):
        for j in range(m):
            line = lines[i].rstrip()
            state[(i,j)] = line[j]

    for _ in range(1000):
        new_state = {}
        for i in range(n):
            for j in range(m):
                new_state[(i,j)] = next_state(i, j, m, n, state)
        state = new_state
        topography = scan_topography(m, n, state)
        print(topography)
    print(topography[Acre.Lumberyard]*topography[Acre.Tree])
# {'.': 1569, '|': 613, '#': 318} pattern is at 1000 and repeats after 28 iterations