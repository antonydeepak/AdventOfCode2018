import re
from collections import deque

def parse(line):
    matches = re.search("(\d+) players; last marble is worth (\d+) points", line)
    return (int(matches[1]),int(matches[2]))

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    line = open(file_name, 'r').readline().rstrip()
    n_players,n_marbles = parse(line)

    players = {}
    for p in range(n_players):
        players[p] = 0

    circle = deque([0])
    p = 0
    for i in range(1, n_marbles+1):
        if i%23 == 0:
            players[p] += i
            circle.rotate(7) # counter-clockwise 7 rotations
            players[p] += circle.popleft()
        else:
            circle.rotate(-2) #clockwise rotation
            circle.appendleft(i)
        # print(f'player:{p} {circle}')
        p = (p+1) % n_players
    print(max(players.values()))