import pygame as pg
from heapq import *
import inspect
import pygame_menu as pm


class Game:

    cols, rows = 23, 13
    TILE = 70

    def __init__(self) -> None:
        pg.init()
        self.sc = pg.display.set_mode([Game.cols * Game.TILE, Game.rows * Game.TILE])
        self.clock = pg.time.Clock()

        grid = ['22222222222222222222212',
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
        self.grid = [[int(char) for char in string ] for string in grid]
      
        self.graph = {}
        self.start = (0, 7)
        self.goal = (22, 7)
        self.queue = []

        heappush(self.queue, (0, self.start))
        self.cost_visited = {self.start: 0}
        self.visited = {self.start: None}

        self.bg = pg.image.load(r'c:\\Users\\Admin\\Desktop\\VS_code\\magic\\MagiCtr\\КР_Системный анализ информационных технологий\\Python-Dijkstra-BFS-A-star-master\\img\\2.png').convert()
        self.bg = pg.transform.scale(self.bg, (Game.cols * Game.TILE, Game.rows * Game.TILE))

    def create_graph(self):

        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

        pass

    def activate_game(self):
        self.sc.blit(self.bg, (0, 0))
        # draw BFS work
        [pg.draw.rect(self.sc, pg.Color('forestgreen'), self.get_rect(x, y), 1) for x, y in self.visited]
        [pg.draw.rect(self.sc, pg.Color('darkslategray'), self.get_rect(*xy)) for _, xy in self.queue]
        pg.draw.circle(self.sc, pg.Color('purple'), *self.get_circle(*self.goal))

        pass

    
    def get_next_nodes(self,x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(self.grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    @classmethod
    def get_circle(cls, x, y):
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
        self.queue=[]
    
    def get_value_graph(self, x):
        return self.graph[x]
    
    def get_cost_visited(self, x=None):
        if x:
            return self.cost_visited[x]
        return self.cost_visited
    
    def set_cost_visited(self,x=None, y=None):
        self.cost_visited[x]=y

    def set_visited(self,x,y):
        self.visited[x] = y

    def get_visited(self,x):
        return  self.visited[x] 
       
    def append_queue(self, x ,y ):
        heappush(self.queue, (x, y))

    def appent_goal(self):
        return heappop(self.get_queue())

    def move_start(self, path_segment):
        pg.draw.circle(self.sc, pg.Color('brown'), *self.get_circle(*path_segment))
        path_segment = self.visited[path_segment]

    def idk(self,x):
        pg.draw.circle(self.sc, pg.Color('blue'), *self.get_circle(*self.start))
        pg.draw.circle(self.sc, pg.Color('magenta'), *self.get_circle(*x))
        
    def ivent_game(self):
        [exit() for event in pg.event.get() if event.type == pg.QUIT]
        pg.display.flip()
        self.clock.tick(7)
        
    






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
        
                    

    def add_button(self,title, font_color, background_color, action=pm.events.EXIT):
        self.mainMenu._theme.widget_alignment = pm.locals.ALIGN_CENTER
        self.mainMenu.add.button(   title=title, action=action, 
                                    font_color=self.return_color(font_color), 
                                    background_color=self.return_color(background_color))
         
        
  
    def add_label(self,title=""):
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
        self.settings.add.button(   title=title, action=action, 
                                    font_color=self.return_color(font_color), 
                                    background_color=self.return_color(background_color))
         
    
        # Text input that takes in the username 
        self.settings.add.text_input(title="User Name : ", textinput_id="username") 

        # 2 different Drop-downs to select the graphics level and the resolution level 
    def return_settings(self):
        return self.settings
    @classmethod
    def return_color(cls, color):
        if color== 'red':
            return cls.RED
        if color== 'green':
            return cls.GREEN
        if color== 'blue':
            return cls.BLUE
        if color== 'cyan':
            return cls.CYAN
        if color== 'black':
            return cls.BLACK
        if color== 'white':
            return cls.WHITE
       
    def show_menu(self):
        self.mainMenu.mainloop(self.screen) 

menu= Menu()
menu.settings()
menu.settings_add_button()
menu.add_button(title= 'Settings', font_color= 'green' , background_color= 'black', action=menu.return_settings())
menu.add_label()
menu.add_button(title= 'Exit', font_color='black', background_color= "white")
menu.show_menu()


























































if False: # __name__ == "__main__"
    game=Game()
    game.create_graph()
    while True:
        game.activate_game()
        if game.get_queue():
            cur_cost, cur_node =game.appent_goal()
            if cur_node == game.get_goal():
                game.set_queue()
                continue
            next_nodes = game.get_value_graph(cur_node)
            for next_node in next_nodes:
                neigh_cost, neigh_node = next_node
                new_cost = game.get_cost_visited(cur_node) + neigh_cost

                if neigh_node not in game.get_cost_visited() or new_cost < game.get_cost_visited(neigh_node):
                    priority = new_cost + game.heuristic(neigh_node, game.goal)
                    game.append_queue(priority, neigh_node)
                    game.set_cost_visited(neigh_node, new_cost)
                    game.set_visited(neigh_node, cur_node)
        # draw path
        path_head, path_segment = cur_node, cur_node
        while path_segment:
            game.move_start(path_segment)
            path_segment =game.get_visited(path_segment)
        
        game.idk(path_head)
        # pygame necessary lines
        game.ivent_game()
