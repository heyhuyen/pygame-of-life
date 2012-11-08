import pdb
import pygame
import random
import sys
from pygame.locals import *

def draw_lines(surface):
    for x in range(1, GRID_SIZE):
        pos = CELL_SIZE * x + LINE_WIDTH/2 + LINE_WIDTH * (x-1)
        pygame.draw.line(surface, GRAY, (pos, 0), (pos, SIZE), LINE_WIDTH)
        pygame.draw.line(surface, GRAY, (0, pos), (SIZE, pos), LINE_WIDTH)

def draw_cell(surface, color, (i, j)):
    # invert coordinates for drawing
    x_pos = j * (CELL_SIZE + LINE_WIDTH)
    y_pos = i * (CELL_SIZE + LINE_WIDTH)
    coords = (x_pos, y_pos, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, coords)

def draw_cells(surface, rects):
    for rect in rects:
        draw_cell(surface, rect[0], rect[1])

def get_cell_indices((x,y)):
    if x in range(1, SIZE-1) and y in range(1, SIZE-1):
        cellnline = (CELL_SIZE + LINE_WIDTH)
        i = y / cellnline
        j = x / cellnline
        if y % cellnline == 0 and x % cellnline == 0:
            return None
        return (i,j)
    return None

# drawing sizes
GRID_SIZE = 4
CELL_SIZE = 50
LINE_WIDTH = 1
SIZE = GRID_SIZE * CELL_SIZE + LINE_WIDTH * (GRID_SIZE - 1)
SCREEN_SIZE = (SIZE, SIZE)

# drawing colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)
BLACK = (0, 0, 0)
BG_COLOR = BLACK 

# cell state colors
ALIVE = GREEN
HOVER = (0, 0, 255)
SELECT = (255, 0, 0)

# use (x, y) for drawing coordinates
# use (i, j) for grid cell indices

if __name__ == "__main__": 
    pygame.init()
    mainclock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('The Game of LIFE')
    live_cells = []
    while True:
        rect_list = []
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                cell = get_cell_indices(event.pos)
                if cell:
                    rect_list.append((HOVER, cell))
            elif event.type == MOUSEBUTTONDOWN:
                cell = get_cell_indices(event.pos)
                if cell:
                    rect_list.append((SELECT, cell))
            elif event.type == MOUSEBUTTONUP:
                cell = get_cell_indices(event.pos)
                if cell:
                    live_cells.append((ALIVE, cell))
        screen.fill(BG_COLOR)
        draw_lines(screen)
        draw_cells(screen, rect_list)
        draw_cells(screen, live_cells)
        pygame.display.update()
        mainclock.tick(10)
