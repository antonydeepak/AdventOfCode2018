import re

def parse(line):
    matches = re.search("(\d+), (\d+)", line)
    return (int(matches[1]), int(matches[2]))

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"
    lines = open(file_name, 'r').read().splitlines()
    points = list(map(parse, lines))
    sort_x = list(sorted(points, key=lambda x: x[0]))
    sort_y = list(sorted(points, key=lambda x: x[1]))
    min_x = sort_x[0][0]
    max_x = sort_x[-1][0]
    min_y = sort_y[0][1]
    max_y = sort_y[-1][1]

    minimum_points = []
    for point in points:
        if point[0]>min_x and point[0]<max_x and point[1]>min_y and point[1]<max_y:
                minimum_points.append(point)

    matrix = {}
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            best_d = max_x+max_y
            best_point = None
            for point in points:
                d = distance((i,j), point)
                if d < best_d:
                    best_d = d
                    best_point = point
                elif d == best_d:
                    best_point = None
            matrix[(i,j)] = best_point
    
    count = {}
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            for point in minimum_points:
                if matrix[(i,j)] == point:
                    if point not in count:
                        count[point] = 0
                    count[point] += 1
    print(max(count.values()))