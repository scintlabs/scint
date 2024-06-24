import heapq


class Space:
    """A location class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    start_location = Space(None, start)
    end_location = Space(None, end)
    open_list = []
    closed_list = []
    heapq.heappush(open_list, start_location)

    while open_list:
        current_location = heapq.heappop(open_list)
        closed_list.append(current_location)
        if current_location == end_location:
            path = []
            current = current_location
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        (x, y) = current_location.position
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            location_position = (x + new_position[0], y + new_position[1])
            if (
                location_position[0] > (len(maze) - 1)
                or location_position[0] < 0
                or location_position[1] > (len(maze[len(maze) - 1]) - 1)
                or location_position[1] < 0
            ):
                continue
            if maze[location_position[0]][location_position[1]] != 0:
                continue
            new_location = Space(current_location, location_position)
            if new_location in closed_list:
                continue
            new_location.g = current_location.g + 1
            new_location.h = (
                (new_location.position[0] - end_location.position[0]) ** 2
            ) + ((new_location.position[1] - end_location.position[1]) ** 2)
            new_location.f = new_location.g + new_location.h
            if any(
                child
                for child in open_list
                if new_location == child and child.g > new_location.g
            ):
                continue
            heapq.heappush(open_list, new_location)

    return None


# Example usage
maze = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]
start = (0, 0)
end = (4, 4)

path = astar(maze, start, end)
print(path)
