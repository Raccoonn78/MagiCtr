"""
Best First Search (greedy algorithm),
always move to the end point, not good with obstacles, can find not the shortest path
"""
import numpy as np
from queue import PriorityQueue
import grid_helper as gh
from pprint import pprint


def find_path_greedy(grid, start, end):
    pq = PriorityQueue() # приоритетная  очередь 
    pq.put((0, start)) # начальнаякоордината 
    came_from = {start: None} # 
    costs = {start: 0}

    while not pq.empty():# 
        current_pos = pq.get()[1]# 

        if current_pos == end:# 
            break
        print(grid)
        print(current_pos[0])
        print(current_pos[1])
        
        neighbors = gh.get_neighbors(grid, current_pos[0], current_pos[1])# 
  
        for neighbor in neighbors:# 
            
            new_cost = costs[current_pos] + gh.get_cost(grid, neighbor)# 
            if neighbor not in costs or new_cost < costs[neighbor] and neighbor not in came_from:# 
            # if neighbor not in came_from:
                costs[neighbor] = new_cost
                priority = gh.heuristic_distance(neighbor, end) # , type="m"
                pq.put((priority, neighbor))# 
                came_from[neighbor] = current_pos# 

    return came_from

def init():
    # initial_grid = gh.generate_grid_empty()
    # initial_grid = gh.generane_my_grid()
    initial_grid = gh.generate_grid_weighted()
    

    start, end = (0, 0), (6, 4)

    came_from = find_path_greedy(initial_grid, start, end)
    path = gh.find_path(start, end, came_from)
    initial_grid= gh.draw_path(path, initial_grid)

    # pprint(initial_grid)
    # print(initial_grid)
    print(np.array(initial_grid))


if __name__ == "__main__":
    init()