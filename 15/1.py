'''
Have to develop a notion of round, move & attack
To track - rounds completed, hit points of individual winning unit
Model
 Unit -> E,G -> to track : attack power, hit point, position
 Board -> Position (x,y), Type (wall, player, space) 
Game is about move and attack
  All units move
  After all units have moved/attacked a round ends
Movement
  For every unit
    Identify range
      Just shortest path from the player. Shortest path also resolves with reading order
      Choose in range
      pick the nearest one - sort by y and then by x.
Attack
   If enemy in range then attack
    deduct 3 from enemy hit point
'''
from collections import deque
from functools import cmp_to_key

class UnitType(object):
    Goblin,Elf = 0,1

class Unit(object):
    def __init__(self, type, position):
        self.type = type
        self.position = position
        self.attack_power = 3
        self.hit_count = 200

direction = [(-1,0), (0,-1), (0,1), (1,0)] #T,L,R,B
def distance(unit_position, board):
    d = {}
    p = {}
    e = set()

    d[unit_position] = 0
    p[unit_position] = unit_position
    e.add(unit_position)

    q = deque([unit_position])
    while len(q)>0:
        parent = q.popleft()
        for heading in direction:
            child = (parent[0]+heading[0], parent[1]+heading[1])
            if board[child] == '.' and child not in e:
                q.append(child)
                d[child] = 1+d[parent]
                p[child] = parent
                e.add(child)

    return d,p

def compare(x,y):
    return (x>y) - (x<y)

def compare_reading(x, y):
    if x[0] == y[0]: #same y coordinate
        return compare(x[1],y[1]) # compare x coordinate
    return compare(x[0],y[0])

def in_range(unit, targets):
    potential_targets = []
    for heading in direction:
        within_range = (unit.position[0]+heading[0],unit.position[1]+heading[1])
        for target in targets:
            if target.position == within_range:
                potential_targets.append(target)

    def compare_attack_reading(x, y):
        if x.hit_count == y.hit_count:
            return compare_reading(x.position, y.position)
        return compare(x.hit_count, y.hit_count)

    potential_targets.sort(key=cmp_to_key(compare_attack_reading))
    return potential_targets

def next_move(unit, units, targets, board):
    # find closest target
        #Enumerate thru all targets and find the in range points
        #find the distance of those in range points from the unit and if there are any choose the top one
        #retract the steps from the chosen in range point and determine the next move
    d,p = distance(unit.position, board)

    if in_range(unit, targets):#already within target; so dont' move
        return unit.position 

    in_ranges = []
    for target in targets:
        for heading in direction:
            within_range = (target.position[0]+heading[0],target.position[1]+heading[1])
            if (within_range in d) and (board[within_range] == '.'):
                in_ranges.append((d[within_range],within_range))
    if not in_ranges: # Not in range of any target. No move needed
        return unit.position

    def compare_distance_reading(x, y):
        distanceX,positionX = x
        distanceY,positionY = y
        if distanceX == distanceY:
            compare_reading(positionX, positionY)
        return compare(distanceX,distanceY)
    in_ranges.sort(key=cmp_to_key(compare_distance_reading))
    target = in_ranges[0][1]

    parent = p[target]
    while parent != unit.position:
        target = parent
        parent = p[target]

    return target

def display(board, n, m):
    for i in range(n):
        hits = []
        for j in range(m):
            v = board[(i,j)]
            if type(v) is Unit:
                hits.append(v.hit_count)
                v = 'G' if v.type == UnitType.Goblin else 'E'
            print(v, end='')
        print(f" {hits}")

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()

    # create board
    board = {}
    units = []
    n = len(lines)
    m = len(lines[0].rstrip())
    for y in range(n): #row
        for x in range(m): #col
            c = (lines[y].rstrip())[x]
            o = c
            if c == 'G':
               o = Unit(UnitType.Goblin, (y,x)) 
               units.append(o)
            elif c == 'E':
               o = Unit(UnitType.Elf, (y,x)) 
               units.append(o)
            board[(y,x)] = o

    victory = False
    i = 0
    while not victory:
        dead_units = set()
        for unit in units:
            if unit in dead_units:
                continue
            live_units = list(filter(lambda x: x not in dead_units, units))
            targets = list(filter(lambda x: (x.type != unit.type), live_units))
            if len(targets) == 0:
                victory = True
                break

            # move, if possible
            move = next_move(unit, live_units, targets, board)
            board[unit.position] = '.'
            board[move] = unit
            unit.position = move

            # attack, if possible
            in_range_targets = in_range(unit, targets)
            if in_range_targets:
                best_target = in_range_targets[0]
                best_target.hit_count -= unit.attack_power
                if best_target.hit_count <= 0:
                    dead_units.add(best_target)
                    board[best_target.position] = '.'
        else: #ignore the current round where they declare victory
            i += 1

        # clean dead units
        for unit in dead_units:
            units.remove(unit)
        units.sort(key=lambda x: cmp_to_key(compare_reading)(x.position))

        display(board, n, m)
        print()

    print(i*sum(unit.hit_count for unit in units))
