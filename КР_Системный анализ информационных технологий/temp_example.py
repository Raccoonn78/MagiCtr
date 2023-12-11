# import pygame
from queue import PriorityQueue
from RP import reconstruct_path,  heuristic


def b_star(grid: object):
    """
    Perform a B* search from start to end.

    Args:
        grid (Grid): An object representing the current grid

    Returns:
        None: The function updates the screen with the search progress and path.
    """

    # Initialize counters and sets
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, grid.start))
    came_from = {}

    # Initialize dictionaries to store the g scores for each node
    g_score = {node: float("inf") for row in grid.grid for node in row}
    g_score[grid.start] = 0

    # Initialize a set to store the nodes in the open set
    open_set_hash = {grid.start}

    # Initialize a flag to track whether the search should continue
   

    # Perform the search
    while not open_set.empty() :#and run:
        # Check for exit events
        # run = check(pygame.event.get(), run)

        # Get the current node from the open set
        _, _, current = open_set.get()
        open_set_hash.remove(current)

        # End the search if the current node is the end node
        if current.is_end():
            # reconstruct_path(came_from, grid.end, grid.draw)
            # grid.end.make_end()
            break

        # Check the neighbors of the current node
        for neighbor in current.neighbors:
            # Calculate the tentative g score for the neighbor
            temp_g_score = g_score[current] + 1

            # Update the g and f scores for the neighbor if the
            # tentative g score is lower
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score

                # Add the neighbor to the open set if it is not already there
                if neighbor not in open_set_hash:
                    f_score = temp_g_score + heuristic("d_manhattan", neighbor, grid.end)
                    count += 1
                    open_set.put((f_score, count, neighbor))
                    open_set_hash.add(neighbor)

                    if not neighbor.is_start() and not neighbor.is_end():
                        neighbor.uncheck()

        

        # Check the current node if it is not the start node
        if not current.is_start():
            current.check()



grid_init = ['22222222222222222222212',
                          '22222292222911112244412',
                          '22444422211112911444412',
                          '24444444212777771444912',
                          '24444444219777771244112',
                          '92444444212777791192144',
                          '22229444212777779111144',
                          '11111112212777772771122',
                          '27722211112777772771244',
                          '27722777712222772221244',
                          '22292777711144429221244',
                          '22922777222144422211944',
                          '22222777229111111119222']

g_score = {node: float("inf") for row in grid_init for node in row}
print(g_score)
# b_star()