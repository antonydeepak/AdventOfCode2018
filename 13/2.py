# Objective is to simulate the ride and find crash spot
# Model : Car, Track
# Car -> Heading(N-Dec y & cons X (0,-1) to position,S,E,W), fork state
# Track -> Kind, location

# Simulation
# List of cars and enumerated in order until crash
# Notion of a crash
# increment in direction of heading? - Add the heading to position
# Loop until a crash

# refer to a map for left in the context of heading. Have a heading -> left,straight,right

import sys

class Cart(object):
    def __init__(self, position, heading):
        self.position = position
        self.heading = heading
        self.next_fork = 0

N = (0,-1)
S = (0,1)
E = (1,0)
W = (-1,0)
intersection_guide = {
    N: [W, N, E], # N -> L,S,R
    S: [E, S, W], # S -> L,S,R
    E: [N, E, S], # E -> L,S,R
    W: [S, W, N], # W -> L,S,R
}
track_guide = {
    '|': {N:N, S:S}, # N stays N & S stays S
    '-': {E:E, W:W}, # E stays E & W stays W
    '/':{W:S, N:E, E:N, S:W}, # W turns S & N turns E
    '\\':{E:S, N:W, W:N, S:E} # E turns S & N turns W
}

def crash(cart, carts):
    for c in carts:
        if c != cart and c.position == cart.position:
            return c
    return None

if __name__ == '__main__':
    # file_name = "test2.in"
    file_name = "1.in"
    lines = open(file_name, 'r').readlines()
    track = {}
    carts = []
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            t = lines[y][x]
            if t == '>' or t == '<':
                track[(x,y)] = '-'
                c = Cart((x,y), E if t=='>' else W)
                carts.append(c)
            elif t == '^' or t == 'v':
                track[(x,y)] = '|'
                c = Cart((x,y), N if t=='^' else S)
                carts.append(c)
            else:
                if ord(t) != '':
                    track[(x,y)] = t
    # print(carts)
    # print(track)
    remaining_carts = set(carts)
    while len(remaining_carts)>1:
        for cart in carts:
            if cart in remaining_carts:
                # change position
                cart.position = (cart.position[0]+cart.heading[0], cart.position[1]+cart.heading[1])

                #change.heading
                t = track[cart.position]
                if t in track_guide:
                    cart.heading = track_guide[t][cart.heading]
                else:
                    assert(t == '+')
                    cart.heading = intersection_guide[cart.heading][cart.next_fork]
                    cart.next_fork = (cart.next_fork+1)%3
                
                crashed = crash(cart, remaining_carts)
                if crashed:
                    # print(remaining_carts)
                    remaining_carts.remove(cart)
                    remaining_carts.remove(crashed)
        # for cart in carts:
        #     print(cart.position, end =' ')
        # print()
    print((remaining_carts.pop()).position)