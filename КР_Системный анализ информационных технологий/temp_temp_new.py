def bellman_ford(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    print('rows',rows)
    print('cols',cols)
    print(grid)
    distance = [[float('inf')] * cols for _ in range(rows)]
    path = [[None] * cols for _ in range(rows)]

    distance[start[0]][start[1]] = 0

    # Relax edges repeatedly
    for _ in range(rows * cols - 1):
        for i in range(rows):
            for j in range(cols):
                if distance[i][j] == float('inf'):
                    continue

                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for xx,yy in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if 0 <= xx < rows and 0 <= yy < cols :
                        if  grid[xx][yy]=='#':
                            neighbors.remove((xx,yy))
                for ni, nj in neighbors:
                    if   0 <= ni < rows and 0 <= nj < cols :
                        # print(grid[ni][nj]  ,grid[ni][nj]!='#' )
                        # if grid[ni][nj]!='#' : 
                            if   distance[i][j] + grid[ni][nj] < distance[ni][nj]:
                                distance[ni][nj] = distance[i][j] + grid[ni][nj]
                                path[ni][nj] = (i, j)

    # Check for negative cycles
    for i in range(rows):
        for j in range(cols):
            if distance[i][j] == float('inf'):
                continue

            neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
            for xx,yy in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if 0 <= xx < rows and 0 <= yy < cols :
                        if  grid[xx][yy]=='#':
                            neighbors.remove((xx,yy))
            for ni, nj in neighbors:
                if  0 <= ni < rows and 0 <= nj < cols:
                    # print(grid[ni][nj], grid[ni][nj]!='#' )
                    # if grid[ni][nj]!='#' : 
                        if  distance[i][j] + grid[ni][nj] < distance[ni][nj]:
                            raise ValueError("Graph contains a negative cycle")

    # Reconstruct the path
    shortest_path = []
    current = end
    print('current',current)
    while current is not None:
        shortest_path.append(current)
        
        current = path[current[0]][current[1]]
    shortest_path.reverse()

    return distance[end[0]][end[1]], shortest_path

def print_paths(paths):
    print("All Paths:")
    for path in paths:
        print(path)
    print("\nShortest Path:")
    print(paths[0])

# Example usage
maze = [[1, 3, 1, 2,3],
        [2, 4000, 1000, 5,      1000000],
        [5, 10000, 200,   3 , 9],
        [5, 10000, 200,   2000,  9],
        [6, 2000, 4,    7,  8]]
maze = ['22222222222222222222212',
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
maze=[  [int(j) for j in i] for i in maze]
start_point =  (5, 0)
end_point = (11, 20)
# start_point = (0, 0)
# end_point = (4, 2)

# try:
#     shortest_distance, all_paths = bellman_ford(maze, start_point, end_point)
#     print(f"Shortest Distance: {shortest_distance}")
#     print_paths(all_paths)
# except ValueError as e:
#     print(e)


import pygame
import sys

def draw_grid(screen, maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            color = (255, 255, 255) if maze[row][col] > 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, (150, 150, 150), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

def draw_path(screen, path, color):
    for node in path:
        pygame.draw.rect(screen, color, (node[1] * cell_size, node[0] * cell_size, cell_size, cell_size))
        pygame.display.flip()
        pygame.time.delay(200)  # Adjust delay for visualization speed

def bellman_ford_visualization(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    distance = [[float('inf')] * cols for _ in range(rows)]
    predecessor = [[None] * cols for _ in range(rows)]

    distance[start[0]][start[1]] = 0

    pygame.init()
    screen_size = (cols * cell_size, rows * cell_size)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Bellman-Ford Visualization")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        draw_grid(screen, maze)

        # Relax edges repeatedly
        for i in range(rows):
            for j in range(cols):
                if distance[i][j] == float('inf'):
                    continue

                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for ni, nj in neighbors:
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if distance[i][j] + maze[ni][nj] < distance[ni][nj]:
                            distance[ni][nj] = distance[i][j] + maze[ni][nj]
                            predecessor[ni][nj] = (i, j)

                            draw_path(screen, [(ni, nj)], (0, 255, 0))

        pygame.display.flip()

        # Check for negative cycles
        for i in range(rows):
            for j in range(cols):
                if distance[i][j] == float('inf'):
                    continue

                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for ni, nj in neighbors:
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if distance[i][j] + maze[ni][nj] < distance[ni][nj]:
                            print("Graph contains a negative cycle")
                            running = False

        pygame.time.delay(500)  # Pause for visualization
        running = False

    # Reconstruct path
    current = end
    path = [current]
    while current != start:
        current = predecessor[current[0]][current[1]]
        path.append(current)

    path.reverse()

    pygame.quit()
    return distance[end[0]][end[1]], path

# Example usage
maze = [[1, 3, 1, 2],
        [2, 4000, 1000, 5],
        [5, 10000, 2, 3],
        [6, 2000, 4, 7]]
maze = ['22222222222222222222212',
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
maze=[  [int(j) for j in i] for i in maze]
start_point =  (5, 0)
end_point = (2, 2)

cell_size = 50  # Adjust the cell size as needed
# shortest_distance, shortest_path = bellman_ford_visualization(maze, start_point, end_point)

# print(f"Shortest Distance: {shortest_distance}")
# print("Shortest Path:", shortest_path)













































import pygame
import sys

def draw_grid(screen, maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            color = (255, 255, 255) if maze[row][col] > 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, (150, 150, 150), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

def draw_path(screen, path, color):
    for node in path:
        pygame.draw.rect(screen, color, (node[1] * cell_size, node[0] * cell_size, cell_size, cell_size))
        pygame.display.flip()
        pygame.time.delay(200)  # Adjust delay for visualization speed

def bellman_ford_visualization(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    distance = [[float('inf')] * cols for _ in range(rows)]
    predecessor = [[None] * cols for _ in range(rows)]

    distance[start[0]][start[1]] = 0

    pygame.init()
    screen_size = (cols * cell_size, rows * cell_size)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Bellman-Ford Visualization")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        draw_grid(screen, maze)

        # Relax edges repeatedly
        for i in range(rows):
            for j in range(cols):
                if distance[i][j] == float('inf'):
                    continue

                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for ni, nj in neighbors:
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if distance[i][j] + maze[ni][nj] < distance[ni][nj]:
                            distance[ni][nj] = distance[i][j] + maze[ni][nj]
                            predecessor[ni][nj] = (i, j)

                            draw_path(screen, [(ni, nj)], (0, 255, 0))

        pygame.display.flip()

        # Check for negative cycles
        for i in range(rows):
            for j in range(cols):
                if distance[i][j] == float('inf'):
                    continue

                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                for ni, nj in neighbors:
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if distance[i][j] + maze[ni][nj] < distance[ni][nj]:
                            print("Graph contains a negative cycle")
                            running = False

        pygame.time.delay(500)  # Pause for visualization
        running = False

    # Reconstruct path
    current = end
    path = [current]
    while current != start:
        current = predecessor[current[0]][current[1]]
        path.append(current)

    path.reverse()

    pygame.quit()
    return distance[end[0]][end[1]], path

# Example usage
maze = ['22222222222222222222212',
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
maze=[  [int(j) for j in i] for i in maze]
start_point =  (5, 0)
end_point = (13, 20)

cell_size = 50  # Adjust the cell size as needed
# shortest_distance, shortest_path = bellman_ford_visualization(maze, start_point, end_point)

# print(f"Shortest Distance: {shortest_distance}")
# print("Shortest Path:", shortest_path)

