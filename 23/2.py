import re

def parse(line):
    matches = re.search("pos=<([-+]?\d+),([-+]?\d+),([-+]?\d+)>, r=([-+]?\d+)", line)
    return (int(matches[1]), int(matches[2]), int(matches[3])), int(matches[4])

def manhattan_distance(a, b):
    x1,y1,z1 = a
    x2,y2,z2 = b
    return abs(x1-x2)+abs(y1-y2)+abs(z1-z2)

if __name__ == '__main__':
    # file_name = "./23/test2.in"
    file_name = "./23/1.in"
    lines = open(file_name, 'r').readlines()

    # This is some crazy ass approximation. We are projecting all the points into a single dimensional
    # distance line and then checking which of those points is covered by the maximum number of bots

    # project all the points into a single dimentional distance line
    distance_line_points = []
    for line in lines:
        coord,signal = parse(line.rstrip())
        distance = manhattan_distance(coord, (0,0,0))
        distance_line_points.append((max(0,distance-signal),distance+signal))

    distances = {}
    for x,y in distance_line_points:
        distances[x] = 0
        distances[y] = 0

    for x in distances:
        for point in distance_line_points:
            if x<=point[1] and x>=point[0]:
                distances[x] += 1
    # it is highely likely that this answer won't be the correct one in that case, I would encourage to
    # try the next best point and so on..
    print(sorted(distances, key=lambda x: (-distances[x],x))[0])