import pygame as pg
from heapq import *
import inspect
import pygame_menu as pm
import numpy as np
from queue import PriorityQueue
import grid_helper as gh
from pprint import pprint
from temp_temp_new import bellman_ford

'''

Напиши код на python который показывает работу алгоритма Беллмана-Форда, 
обязательно с реализацией отрицательных весов во взвешенном графе  для прохождением лабиринта . 
Лабиринт в исходном виде состоит из вложенных списков , в котором указаны веса каждой из точек.
Найти кратчайший путь введенный пользователем в этом лабиринте.
Программа так же должна выводить все варианты путей до конечной точки и отдельно выводила самый кратчайший путью.
Пришли код программы  одним сообщением , перед отправкой проверь на работоспособность , вводя в качестве тестовых значений случайные числа от 0 до 4, 
если выявится ошибка в ходе выполнения этих тестов , исправь код , проверь еще раз и пришли код одним сообщением.

'''

class Graph:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.V = self.rows * self.cols
        self.graph = []
        

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def convert_to_vertex(self, i, j):
        return i * self.cols + j

    def bellman_ford(self, src, dest):
        dist = [float("Inf")] * self.V
        dist[src] = 0

        for _ in range(self.V - 1):
            for i in range(self.rows):
                for j in range(self.cols):
                    u = self.convert_to_vertex(i, j)
                    if i > 0:
                        v = self.convert_to_vertex(i - 1, j)
                        w = self.maze[i - 1][j]
                        if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                            dist[v] = dist[u] + w
                    if i < self.rows - 1:
                        v = self.convert_to_vertex(i + 1, j)
                        w = self.maze[i + 1][j]
                        if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                            dist[v] = dist[u] + w
                    if j > 0:
                        v = self.convert_to_vertex(i, j - 1)
                        w = self.maze[i][j - 1]
                        if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                            dist[v] = dist[u] + w
                    if j < self.cols - 1:
                        v = self.convert_to_vertex(i, j + 1)
                        w = self.maze[i][j + 1]
                        if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                            dist[v] = dist[u] + w

        return {'1':dist[dest], '2':dist}
    
    def get_shortest_path(self, src, dest, dist, path, shortest_path, current_path):
        if src == dest:
            current_path.append(dest)
            if dist[dest] < shortest_path[0]:
                shortest_path[0] = dist[dest]
                shortest_path[1] = current_path.copy()
            return #(src, dest, dist, path, shortest_path, current_path)

        for edge in self.graph:
            u, v, w = edge
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                path[v] = u
                self.get_shortest_path(u, dest, dist, path, shortest_path, current_path)
                dist[v] = float("Inf")
                path[v] = -1
        
    def print_all_paths(self, paths):
        for i in range(len(paths)):
            print(f"Путь {i + 1}: {paths[i]}")

    def find_shortest_path(self, src, dest, dist):
        # dist = [float("Inf")] * self.V
        # dist[src] = 0
        print(dist)
        path = [-1] * self.V
        shortest_path = [float("Inf"), []]
        current_path = []

        # src, dest, dist, path, shortest_path, current_path =
        self.get_shortest_path(src, dest, dist, path, shortest_path, current_path)

        # paths = []
        temp_dest = dest
        while temp_dest != -1:
            path.append(temp_dest)
            temp_dest = path[temp_dest]

        path.reverse()
        self.print_all_paths(path)
        print(f"Самый кратчайший путь: {shortest_path[1]}, длина: {shortest_path[0]}")

# Пример лабиринта (матрица с весами каждой точки)
maze = [
    [1, 3, 1, 2],
    [2, 4000, 1000, 5],
    [5, 10000, 2, 3],
    [6, 2000, 4, 7]
]

# Создаем граф на основе лабиринта
g = Graph(maze)

# Получаем координаты начальной и конечной точек от пользователя
# start_i, start_j = map(int, input("Введите координаты начальной точки (номер строки и номер столбца через пробел): ").split())
# end_i, end_j = map(int, input("Введите координаты конечной точки (номер строки и номер столбца через пробел): ").split())


# Запускаем алгоритм Беллмана-Форда для поиска кратчайшего пути
# src = g.convert_to_vertex(start_i, start_j)
# dest = g.convert_to_vertex(end_i, end_j)
# print(dest)
# shortest_path_length = g.bellman_ford(src, dest)
# g.find_shortest_path(src, dest, shortest_path_length['2'])
# print(f"Кратчайший путь от начальной до конечной точки: {shortest_path_length}")
# # Запускаем алгоритм для поиска всех путей и кратчайшего пути
# src = g.convert_to_vertex(start_i, start_j)
# dest = g.convert_to_vertex(end_i, end_j)
# g.find_shortest_path(src, dest)

class Game:

    cols, rows = 23, 13
    TILE = 70

    def __init__(self) -> None:
        self.block_dict={}
        self.grid_init = ['22222222222222222222212',
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
        self.maze=[  [int(j) for j in i] for i in self.grid_init]
        self.grid_m= [  [j for j in i.replace('4','9') ] for i in self.grid_init]
        self.size_grid= {
            'Дорога':'1',
            'Пустошь':'2',
            'Река':'7',
            'Камень':'9',                        
            'Куст':'9',                        
            'Трава':'4',                        
                         }
        """
        КУСТ 
        КАМЕНЬ
        РЕКА
        ДОРОГА 
        дорогу можно настроить самому, пустые поля будут дефолтные , камень будет весит 1000000
        для того чтобы срабатывал фактор проходимости , так же река и куст 
        """

    def create_graph(self):
        pg.init()
        self.sc = pg.display.set_mode(
            [Game.cols * Game.TILE, Game.rows * Game.TILE])
        self.clock = pg.time.Clock()
        self.grid = [[int(char) for char in string]
                     for string in self.grid_init]
        self.graph = {}
        self.start = (0, 7)
        self.goal = (0, 7)
        self.queue = []
        self.block= [(-1,-1)]
        self.unblock= (-1,-1)

        heappush(self.queue, (0, self.start))
        self.cost_visited = {self.start: 0}
        self.visited = {self.start: None}

        self.bg = pg.image.load(  
            r'c:\\Users\\Admin\\Desktop\\VS_code\\magic\\MagiCtr\\КР_Системный анализ информационных технологий\\Python-Dijkstra-BFS-A-star-master\\img\\2.png').convert()
        # c:\\Users\\Дмитрий\\Desktop\\МАГИСТР\\MagiCtr\\КР_Системный анализ информационных технологий\\Python-Dijkstra-BFS-A-star-master\\img\\2.png
        #    C:\Users\Дмитрий\Desktop\МАГИСТР\MagiCtr\КР_Системный анализ информационных технологий\main_file.py
            # r'c:\\Users\\Admin\\Desktop\\VS_code\\magic\\MagiCtr\\КР_Системный анализ информационных технологий\\Python-Dijkstra-BFS-A-star-master\\img\\2.png').convert()

        self.bg = pg.transform.scale(
            self.bg, (Game.cols * Game.TILE, Game.rows * Game.TILE))

        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                self.graph[(x, y)] = self.graph.get(
                    (x, y), []) + self.get_next_nodes(x, y)

        pass

    def activate_game(self):
        self.sc.blit(self.bg, (0, 0))
        # draw BFS work
        [pg.draw.rect(self.sc, pg.Color('red'),
                      self.get_rect(x, y), 1) for x, y in self.visited]
        [pg.draw.rect(self.sc, pg.Color('darkslategray'),
                      self.get_rect(*xy)) for _, xy in self.queue]
        pg.draw.circle(self.sc, pg.Color('purple'),
                       *self.get_circle(*self.goal))
        if self.block:
            # print(self.block)
            [pg.draw.circle(self.sc, pg.Color('black'),
                        *self.get_circle(*xy))  for xy in self.block]
            # [pg.draw.rect(self.sc, pg.Color('black'),
            #           self.get_rect(*xy)) for  xy in self.block]
            
        # pg.draw.circle(self.sc, pg.Color('black'),
        #                *self.get_circle(*self.block, 0))

        pass

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(self.grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def custom_map(self):
        print('Хотите сделать карту кастомной?\n1-Дефолт\n2-Свои параметры')
        check = input('Введите вариант ответа:').strip()
        a = 0
        while not check.isdigit() and ' ' in check:
            check = input('Введите вариант ответа:').strip()
            a += 1
            if a == 10:
                return {'code': 0, 'message': 'ОЙ ВСЁ'}
            
        if int(check) == 1:
            return {'code':1,
                    'message': 'Дефолтный варинт'}
        elif int(check) == 2:
            temp = self.set_graph_size()
            if temp['code'] == 1:
                print(self.grid_init)
                return {'code':1,
                        'message': 'Карта была изменена'}
            else:
                return {'code': 0 ,
                        'message':temp['message']}

    def out_put_message(self, message):
        check = input(f'{message}')
        a = 0
        while not check.isdigit() or (' ' in check) or (not eval(f'-1<{check}<10')):
            check = input('Введите число от 0 до 9:').strip()
            a+=1
            if a == 10: return {'code': 0, 
                                'message': 'ОЙ ВСЁ' }
        return {'code': 1,
                'message': f'ok',
                'data': check }

    def set_graph_size(self):
        message_list = ['Введите вес для дороги от 0 до 9:',  'Введите вес для пустоши от 0 до 9:',
                        'Введите вес для реки от 0 до 9:',    'Введите вес для камня от 0 до 9:',
                        'Введите вес для кустов от 0 до 9:',  'Введите вес для травы от 0 до 9:' ]
        for key, message in zip(self.size_grid.keys(),message_list):
            check = self.out_put_message(message)
            if check['code'] == 1:
                self.grid_init=[ x.replace(self.size_grid[key],check['data'] )  for x in self.grid_init]
            elif check['code']==0:return check
        else: return check
        

    @classmethod
    def get_circle(cls, x, y, zero=None):
        if zero: return (x * cls.TILE + cls.TILE // 2, y * cls.TILE + cls.TILE // 2),0
        return (x * cls.TILE + cls.TILE // 2, y * cls.TILE + cls.TILE // 2), cls.TILE // 4

    @classmethod
    def get_rect(cls, x, y):
        return x * cls.TILE + 1, y * cls.TILE + 1, cls.TILE - 2, cls.TILE - 2

    @classmethod
    def heuristic(cls, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_goal(self):
        return self.goal

    def get_queue(self):
        return self.queue

    def set_queue(self):
        self.queue = []

    def get_value_graph(self, x):
        return self.graph[x]

    def get_cost_visited(self, x=None):
        if x:
            return self.cost_visited[x]
        return self.cost_visited

    def set_cost_visited(self, x=None, y=None):
        self.cost_visited[x] = y

    def set_visited(self, x, y):
        self.visited[x] = y

    def set_abs_visited(self, visited):
        self.visited = visited

    def get_visited(self, x):
        return self.visited[x]

    def append_queue(self, x, y):
        heappush(self.queue, (x, y))

    def appent_goal(self):
        return heappop(self.get_queue())

    def move_start(self, path_segment):
        pg.draw.circle(self.sc, pg.Color('red'), *
                       self.get_circle(*path_segment))
        path_segment = self.visited[path_segment]

    def idk(self, x):
        pg.draw.circle(self.sc, pg.Color('blue'), *
                       self.get_circle(*self.start))
        pg.draw.circle(self.sc, pg.Color('magenta'), *self.get_circle(*x))

    def ivent_game(self):
        [exit() for event in pg.event.get() if event.type == pg.QUIT]
        pg.display.flip()
        self.clock.tick(7)

    def get_click_mouse_pos(self, butt):
        click = pg.mouse.get_pressed()
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.TILE, y // self.TILE
        pg.draw.circle(self.sc, pg.Color('red'), * self.get_circle(grid_x, grid_y))

        if click[0] and butt=="l":
            x, y = pg.mouse.get_pos()
            grid_x, grid_y = x // self.TILE, y // self.TILE
            pg.draw.circle(self.sc, pg.Color('red'), *
                        self.get_circle(grid_x, grid_y))
            
            # print('click',click)
            return (grid_x, grid_y)
        
        if click[2] and butt=="r":
            
            x, y = pg.mouse.get_pos()
            grid_x, grid_y = x // self.TILE, y // self.TILE
            if (grid_x, grid_y) not in self.block:
                pg.draw.circle(self.sc, pg.Color('black'), *
                        self.get_circle(grid_x, grid_y))
            
            # print('click',click)
            
                self.block.append( (grid_x, grid_y))
                self.block_dict[(grid_y,grid_x)]=self.maze[grid_y][grid_x]
                self.maze[grid_y][grid_x]='#'
                
                return (grid_x, grid_y)
            else:
                return False
        
        if click[1] and butt=="m":
            # img = pg.font.render(self., True, RED)
            # rect = img.get_rect()
            # pygame.draw.rect(img, BLUE, rect, 1)
            
            x, y = pg.mouse.get_pos()
            grid_x, grid_y = x // self.TILE, y // self.TILE
            if (grid_x, grid_y)  in self.block:
                pg.draw.circle(self.sc, pg.Color('black'), *
                            self.get_circle(grid_x, grid_y))
                
                # self.unblock = (grid_x, grid_y)
                self.block.remove((grid_x, grid_y))
                self.maze[grid_y][grid_x]=self.block_dict[(grid_y,grid_x)]
                return (grid_x, grid_y)

        return  False
    
    def get_click_right(self):
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.TILE, y // self.TILE
        pg.draw.circle(self.sc, pg.Color('red'), *
                       self.get_circle(grid_x, grid_y))
        click = pg.mouse.get_pressed()

        return (grid_x, grid_y) if click[0] else False

    def dijkstra(self, start, goal, graph):
        self.goal = goal
        self.queue = []
        self.start = start
        self.graph = graph

        heappush(self.queue, (0, self.start))
        cost_visited = {self.start: 0}
        visited = {self.start: None}

        while self.queue:
            cur_cost, cur_node = heappop(self.queue)
            if cur_node == self.goal:
                break

            neighbours = self.graph[cur_node]

            for neighbour in neighbours:
                neigh_cost, neigh_node = neighbour
                new_cost = cost_visited[cur_node] + neigh_cost

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    priority = new_cost + self.heuristic(neigh_node, self.goal)
                    heappush(self.queue, (priority, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node
        return visited

    def find_path_greedy(self, grid, start, end):
       
        self.pq = PriorityQueue() # приоритетная  очередь 
        self.pq.put((0, start)) # начальнаякоордината 
        self.start=start
        self.goal=end
        self.graph=grid
        self.came_from = {self.start: None} # 
        self.costs = {self.start: 0}
        print(start)
        print({self.start: None})
        print({self.start: 0})
        print(end)
        while not self.pq.empty():# 
            # print('self.pq.queue>>>',list(self.pq.queue))
            current_pos = self.pq.get()[1]# 
            print('current_pos',current_pos, 'list', list(self.pq.queue))

            if current_pos == self.goal:# 
                break
            # print('len(self.graph)',len(self.graph))
            # print('len(self.graph)[01]',len(self.graph[0]))
            neighbors = gh.get_neighbors(self.graph  , current_pos[0], current_pos[1])# 
    
            for neighbor in neighbors:# 
                neigh_cost, neigh_node = neighbor
                new_cost = self.costs[current_pos] + gh.get_cost(grid, neighbor)# 
                # if neighbor not in self.costs or new_cost < self.costs[neighbor] :#  and neighbor not in self.came_from
                # print('neighbor',neighbor)
                
                if neighbor not in self.came_from:
                    # print('self.came_from',self.came_from)
                    
                    print('neighbor',neighbor, 'neighbors', neighbors)
                    self.costs[neighbor] = new_cost
                    priority = gh.heuristic_distance(neighbor, self.goal, type='m') # , type="m"
                    self.pq.put((priority, neighbor))# 
                    self.came_from[neighbor] = current_pos# 
            self.queue = list(self.pq.queue)
        print('self.pq.empty()',self.pq.empty())
        return self.came_from


class Menu:
    WIDTH, HEIGHT = 900, 600
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 100, 100)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((Menu.WIDTH, Menu.HEIGHT))
        self.mainMenu = pm.Menu(title="Menu",
                                width=Menu.WIDTH,
                                height=Menu.HEIGHT,
                                theme=pm.themes.THEME_DARK)

    def add_button(self, title, font_color, background_color, action=pm.events.EXIT):
        self.mainMenu._theme.widget_alignment = pm.locals.ALIGN_CENTER
        self.mainMenu.add.button(title=title, action=action,
                                 font_color=self.return_color(font_color),
                                 background_color=self.return_color(background_color))

    def add_label(self, title=""):
        self.mainMenu.add.label(title=title)

    def settings(self):
        self.settings = pm.Menu(title="Settings",
                                width=Menu.WIDTH,
                                height=Menu.HEIGHT,
                                theme=pm.themes.THEME_DARK)
        self.settings._theme.widget_font_size = 55
        self.settings._theme.widget_font_color = Menu.BLACK
        self.settings._theme.widget_alignment = pm.locals.ALIGN_LEFT

    def settings_add_button(self, title='', font_color='white', background_color='black', action=None):
        self.settings.add.clock(clock_format="%d-%m-%y %H:%M:%S",
                                title_format="Local Time : {0}")
        self.settings.add.button(title=title, action=action,
                                 font_color=self.return_color(font_color),
                                 background_color=self.return_color(background_color))

        # Text input that takes in the username
        self.settings.add.text_input(
            title="User Name : ", textinput_id="username")

        # 2 different Drop-downs to select the graphics level and the resolution level
    def return_settings(self):
        return self.settings

    @classmethod
    def return_color(cls, color):
        if color == 'red':
            return cls.RED
        if color == 'green':
            return cls.GREEN
        if color == 'blue':
            return cls.BLUE
        if color == 'cyan':
            return cls.CYAN
        if color == 'black':
            return cls.BLACK
        if color == 'white':
            return cls.WHITE

    def show_menu(self):
        self.mainMenu.mainloop(self.screen)

# menu= Menu()
# menu.settings()
# menu.settings_add_button()
# menu.add_button(title= 'Settings', font_color= 'green' , background_color= 'black', action=menu.return_settings())
# menu.add_label()
# menu.add_button(title= 'Exit', font_color='black', background_color= "white")
# menu.show_menu()


if True:  # __name__ == "__main__"
    game = Game()
    while_true = False
    temp = game.custom_map()

    if temp['code'] == 1:
        while_true = True
        game.create_graph()
        visited = {game.start: None}
    # maze = game.grid_init
    # maze=[  [int(j) for j in i] for i in maze]
    print(temp['message'])
    """
        КУСТ 
        КАМЕНЬ
        РЕКА
        ДОРОГА 
        дорогу можно настроить самому, пустые поля будут дефолтные , камень будет весит 1000000
        для того чтобы срабатывал фактор проходимости , так же река и куст 
    """
    
    while while_true:
        game.activate_game()
        # if game.get_queue():
        #     cur_cost, cur_node =game.appent_goal()
        #     if cur_node == game.get_goal():
        #         game.set_queue()
        #         continue
        #     next_nodes = game.get_value_graph(cur_node)
        #     for next_node in next_nodes:
        #         neigh_cost, neigh_node = next_node
        #         new_cost = game.get_cost_visited(cur_node) + neigh_cost

        #         if neigh_node not in game.get_cost_visited() or new_cost < game.get_cost_visited(neigh_node):
        #             priority = new_cost + game.heuristic(neigh_node, game.goal)
        #             game.append_queue(priority, neigh_node)
        #             game.set_cost_visited(neigh_node, new_cost)
        #             game.set_visited(neigh_node, cur_node)
        # draw path
        
        mouse_pos = game.get_click_mouse_pos('l') # выбор позиции 
        mouse_right = game.get_click_mouse_pos('r') # выбор позиции
        mouse_midle = game.get_click_mouse_pos('m') # выбор позиции

        if mouse_pos:
            # visited = game.dijkstra(game.start, mouse_pos, game.graph) # start, goal, graph
            # visited = game.find_path_greedy(start=game.start, end=mouse_pos, grid=game.grid_m) # start, goal, graph
            print(game.maze)
            shortest_distance, all_paths = bellman_ford(game.maze, game.start[::-1], mouse_pos[::-1])
            
            visited={ all_paths[i][::-1]:all_paths[i+1][::-1]  for i in range(len(all_paths)-1) }
            game.set_abs_visited(visited)
            game.goal = mouse_pos
            game.queue=[(i,all_paths[i][::-1]) for i in range(len(all_paths))]

        path_head, path_segment = game.goal, game.goal
        while path_segment and path_segment in visited:
            game.move_start(path_segment) # 
            # print('path_segment',path_segment)
            path_segment = game.get_visited(path_segment)
         
        game.idk(path_head)
        game.ivent_game()
