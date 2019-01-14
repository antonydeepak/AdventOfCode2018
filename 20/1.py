import operator

class Room(object):
    def __init__(self, location, distance):
        self.location = location
        self.distance = distance #measures no. of doors from origin

class Markers(object):
    NavStart,NavEnd,SplitStart,SplitEnd,BranchEnd = ('^', '$', '(', ')', '|')

directions = {'N': (0,-1), 'S': (0,1), 'E': (1,0), 'W': (-1,0)} #N,S,E,W

def next_position(location, direction):
    return tuple(map(operator.add, location, direction))

def navigate(rooms, split_room, navigation_map, navigation_point):
    n = len(navigation_map) 
    cur_room = split_room

    while navigation_point < n:
        d = navigation_map[navigation_point]
        if d == Markers.NavStart:
            room = Room((0,0), 0)
            rooms[(0,0)] = room
            cur_room = room
        elif d == Markers.NavEnd:
            assert(split_room == None) #assert we see NavEnd at the first level of recursion
            return navigation_point
        elif d == Markers.SplitStart:
            navigation_point = navigate(rooms, cur_room, navigation_map, navigation_point+1)
        elif d == Markers.SplitEnd:
            assert(split_room != None) #assert we see SplitEnd at the second or higher levels of recursion
            return navigation_point
        elif d == Markers.BranchEnd:
            cur_room = split_room
        elif d in directions:
            # door; don't care
            position = next_position(cur_room.location, directions[d])

            # room
            position = next_position(position, directions[d])
            room = Room(position, cur_room.distance+1)  
            if position in rooms:
                room.distance = min(rooms[position].distance, room.distance) #shortest distance
            rooms[position] = room
            cur_room = room
        else:
            raise "Unknown nav point"
        navigation_point += 1

if __name__ == '__main__':
    # file_name = "test.in"
    file_name = "1.in"

    rooms = {}
    navigation_map = open(file_name, 'r').readline().rstrip()
    navigate(rooms, None, navigation_map, 0)
    # part 1
    print(max(rooms[room].distance for room in rooms))
    # part 2
    print(len([room for room in rooms if (rooms[room].distance >= 1000)]))
