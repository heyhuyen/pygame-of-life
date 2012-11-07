import pdb
import pygame
import random
import sys

GRID_SIZE = 50
CELL_SIZE = 10
LINE_WIDTH = 1
SIZE = GRID_SIZE * CELL_SIZE + LINE_WIDTH * (GRID_SIZE - 1)
SCREEN_SIZE = (SIZE, SIZE)

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)
BLACK = (0, 0, 0)
BG_COLOR = BLACK 

def draw_lines(surface):
    for x in range(1, GRID_SIZE):
        pos = CELL_SIZE * x + LINE_WIDTH/2 + LINE_WIDTH * (x-1)
        pygame.draw.line(surface, GRAY, (pos, 0), (pos, SIZE), LINE_WIDTH)
        pygame.draw.line(surface, GRAY, (0, pos), (SIZE, pos), LINE_WIDTH)

def draw_live_cell(surface, (x,y)):
    x_pos = x*(CELL_SIZE + LINE_WIDTH)
    y_pos = y*(CELL_SIZE + LINE_WIDTH)
    coords = (x_pos, y_pos, CELL_SIZE, CELL_SIZE)
    #live_list.append(pygame.draw.rect(surface, GREEN, coords))
    pygame.draw.rect(surface, GREEN, coords)

#live_list = []

if __name__ == "__main__": 
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('The Game of LIFE')
    screen.fill(BG_COLOR)
    draw_lines(screen)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #if len(live_list) > 0:
        #    live_list[-1].
        draw_live_cell(screen, (random.choice(range(0,GRID_SIZE)), random.choice(range(0, GRID_SIZE))))
        pygame.display.update()
        #live_list.pop()
