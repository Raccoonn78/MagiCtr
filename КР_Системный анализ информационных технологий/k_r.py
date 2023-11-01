

"""
Метод создания карты	| Учет проходимости	   |Разбиение карты 	|Учет топлива	|Радиус поворота 	|Видимость	    |Алгоритм |
----------------------------------------------------------------------------------------------------------------------------------|
Ручная	                |  Да	               |   Квадратный	    | Нет	        |Нет	            |Бесконечная	|   B*    |

"""

import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка от Skillbox')
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15
font_style = pygame.font.SysFont("bahnschrift", 25) #Укажем название шрифта и его размер для системных сообщений, например, при завершении игры.
score_font = pygame.font.SysFont("comicsansms", 35) #Укажем шрифт и его размер для отображения счёта. Это мы реализуем очень скоро.
 
def our_snake(snake_block, snake_list):
   for x in snake_list:
       pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
def message(msg, color):
   mesg = font_style.render(msg, True, color)
   dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
 
def gameLoop():
   game_over = False
   game_close = False
   x1 = dis_width / 2
   y1 = dis_height / 2
   x1_change = 0
   y1_change = 0
   snake_List = [] #Создаём список, в котором будем хранить показатель текущей длины змейки.
   Length_of_snake = 1 
   foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
   foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
   while not game_over:
       while game_close == True:
           dis.fill(blue)
           message("Вы проиграли! Нажмите Q для выхода или C для повторной игры", red)
           pygame.display.update()
           for event in pygame.event.get():
               if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_q:
                       game_over = True
                       game_close = False
                   if event.key == pygame.K_c:
                       gameLoop()
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
            if x1 >= (dis_width-200) :
                y1_change = 10
                x1_change = 0
            elif x1 < 250 : 
                y1_change = 10
                x1_change = 0
            if y1 >= (dis_height-200) :
                x1_change = -10
                y1_change = 0
            elif y1 < 250 :
                x1_change = 10
                y1_change = 0
                

       x1 += x1_change
       y1 += y1_change
       dis.fill(blue)
       
       snake_Head = [] #Создаём список, в котором будет храниться показатель длины змейки при движениях.
       snake_Head.append(x1) #Добавляем значения в список при изменении по оси х.
       snake_Head.append(y1) #Добавляем значения в список при изменении по оси y.
       snake_List.append(snake_Head)
  
       our_snake(snake_block, snake_List)
       pygame.display.update()

       Length_of_snake += 1    
       clock.tick(snake_speed)
   pygame.quit()
   quit()
 
gameLoop()