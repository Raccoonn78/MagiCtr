"""
S - start point
E - end point
x - visited
@ - path
# - obstacle
1 - cost
"""

import math

START_COL = "S"
END_COL = "E"
VISITED_COL = "x"
OBSTACLE_COL = "#"
PATH_COL = "@"


def generane_my_grid():
    grid_init = [       "22222222222222222222212",
                        "22222292222911112244412",
                        "22444422211112911444412",
                        "24444444212777771444912",
                        "24444444219777771244112",
                        "92444444212777791192144",
                        "22229444212777779111144",
                        "11111112212777772771122",
                        "27722211112777772771244",
                        "27722777712222772221244",
                        "22292777711144429221244",
                        "22922777222144422211944",
                        "22222777229111111119222"]
    grid_m= [  [j for j in i] for i in grid_init]
    
    return grid_m


def generate_grid_empty():
    return [[".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."]]


def generate_grid_obstacle():
    return [[".", ".", "#", ".", ".", ".", ".", ".", "."],
            [".", ".", "#", ".", "#", ".", ".", ".", "."],
            [".", ".", ".", ".", "#", ".", ".", ".", "."],
            [".", ".", "#", ".", "#", ".", ".", ".", "."],
            [".", ".", "#", ".", ".", ".", ".", ".", "."],
            [".", ".", "#", ".", "#", ".", ".", ".", "."],
            [".", ".", "#", "#", "#", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."]]


def generate_grid_obstacle_for_b_star():
    """
    worst obstacle for B*
    """

    return [[".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "#", "#", "#", "#", "#", "#", "#", "."],
            [".", ".", ".", ".", ".", ".", ".", "#", "."],
            [".", ".", ".", ".", ".", ".", ".", "#", "."],
            [".", ".", ".", ".", ".", ".", ".", "#", "."],
            [".", ".", ".", ".", ".", ".", ".", "#", "."],
            [".", ".", ".", ".", ".", ".", ".", "#", "."],
            [".", "#", "#", "#", "#", "#", "#", "#", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."]]


def generate_grid_weighted():
    """
    weighted grid
    """

    return [[".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "#", "#", "#", "#", ".", "#", "#", "."],
            [".", ".", "2", "1", "9", ".", ".", "#", "."],
            [".", ".", "9", "2", "2", ".", ".", "#", "."],
            [".", ".", "9", "2", "100", ".", ".", "#", "."],
            [".", ".", "2", "9", "9", ".", ".", "#", "."],
            [".", ".", "9", "9", "9", ".", ".", "#", "."],
            [".", "#", "#", "#", "#", "#", "#", "#", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."]]


def heuristic_distance(pos, end_pos, type="e"):
    """
    m - manhattan
    e - euclidean
    """

    dx = abs(pos[0] - end_pos[0])
    dy = abs(pos[1] - end_pos[1])

    if type == "m":
        return dx + dy

    return math.sqrt(dx * dx + dy * dy)


def find_path(start, end, came_from):
    """Find the shortest path from start to end point"""

    path = [end]

    current = end
    while current != start:
        current = came_from[current]
        path.append(current)

    # reverse to have Start -> Target
    # just looks nicer
    path.reverse()

    return path


def get_cost(grid, pos):
    col_val = grid[pos[0]][pos[1]]
    return int(col_val) if col_val.isdigit() else 1


def get_neighbors(grid,  col,row):
    height = len(grid)  # 13  
    width = len(grid[0]) # 23 
    print('height',height)
    print('width',width)
    neighbors = [( col ,row + 1), ( col - 1, row), (col, row - 1), ( col + 1, row)]

    # make path nicer
    # if (row + col) % 2 == 0:
    #     neighbors.reverse()

    # check borders
    print('neighbors',neighbors)
    print('row',row)
    print('col',col)

    neighbors = list(filter(lambda t: (0 <= t[0] <height  and 0 <= t[1] < width), neighbors))
    # check obstacles
    print('neighbors_2',list(neighbors))
    print(grid)
    print(list(neighbors))
    neighbors = list(filter(lambda t: (grid[t[0]][t[1]] != OBSTACLE_COL), neighbors))
    print('neighbors_3',list(neighbors))

    return neighbors


def draw_path(path, grid):
    for row, col in path:
        grid[row][col] = PATH_COL

    # draw start and end
    start_pos = path[0]
    end_pos = path[-1]
    grid[start_pos[0]][start_pos[1]] = START_COL
    grid[end_pos[0]][end_pos[1]] = END_COL

    return grid