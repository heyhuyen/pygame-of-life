import pygame
from pygame.locals import *
import event_manager
import pdb

# drawing sizes
GRID_SIZE = 10
CELL_SIZE = 50
LINE_WIDTH = 1
SIZE = GRID_SIZE * CELL_SIZE + LINE_WIDTH * (GRID_SIZE - 1)
SCREEN_SIZE = (SIZE, SIZE)

# drawing colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BG_COLOR = BLACK 
LINE_COLOR = GRAY

# cell state colors
COLORS = [RED, GREEN, BLUE]
SELECT = 0
ALIVE = 1
HOVER = 2

# use (x, y) for drawing coordinates
# use (i, j) for grid cell indices

class PygameView:
    
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('The Game of LIFE')
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BG_COLOR)
        self.screen.blit(self.background, (0,0))
        self.draw_lines(self.screen)

        self.live_sprites = pygame.sprite.RenderUpdates()
        self.selected = pygame.sprite.RenderUpdates()
        self.cursor = pygame.sprite.GroupSingle()
       
        pygame.display.update() 

    def refresh_live_sprites(self, live_cells):
        self.live_sprites.empty()
        for cell in live_cells:
            newSprite = CellSprite(ALIVE, cell, self.live_sprites)

    def notify(self, event):
        if isinstance(event, event_manager.TickEvent):
            # Draw everything
            self.live_sprites.clear(self.screen, self.background)
            self.selected.clear(self.screen, self.background)
            self.cursor.clear(self.screen, self.background)

            self.live_sprites.update()
            self.selected.update()

            live_list = self.live_sprites.draw(self.screen) 
            cursor = self.cursor.draw(self.screen)
            select_list = self.selected.draw(self.screen)
            
            pygame.display.update()
        elif isinstance(event, event_manager.QuitEvent):
            pygame.quit()
        elif isinstance(event, event_manager.UniverseConfiguredEvent):
            self.refresh_live_sprites(event.universe.live_cells)
        elif isinstance(event, event_manager.EvolveEvent):
            self.refresh_live_sprites(event.live_cells)
        elif isinstance(event, event_manager.ConfigureEvent):
            self.refresh_live_sprites(event.live_cells)
        elif isinstance(event, event_manager.HoverEvent):
            self.hover(event.pos)
        elif isinstance(event, event_manager.SelectStartEvent):
            self.select_start(event.pos)
        elif isinstance(event, event_manager.SelectEndEvent):
            cell_list = self.select_end(event.pos)
            cell_list = list(set(cell_list))
            ev = event_manager.ConfigureRequest(cell_list)
            self.event_manager.post(ev)

    def hover(self, pos):
        cell = self.get_cell_indices(pos)
        if cell:
            if len(self.selected) == 0:
                cell_sprite = CellSprite(HOVER, cell, self.cursor)
            else:
                #check here
                cell_sprite = CellSprite(SELECT, cell, self.selected)
                #collisions = pygame.sprite.spritecollideany(cell_sprite, self.selected)

    def select_start(self, pos):
        cell = self.get_cell_indices(pos)
        if cell:
            #check here
            cell_sprite = CellSprite(SELECT, cell, self.selected)

    def select_end(self, pos):
        cell = self.get_cell_indices(pos)
        if cell:
            cell_sprite = CellSprite(SELECT, cell, self.selected) 
            #for thing in self.selected:
                #thing.state = ALIVE
                #self.live_sprites.add(thing)
        cell_list = [cell.coords for cell in self.selected]
        self.selected.empty()
        self.cursor.empty()
        return cell_list

    def get_cell_indices(self, (x,y)):
        if x in range(1, SIZE-1) and y in range(1, SIZE-1):
            cellnline = (CELL_SIZE + LINE_WIDTH)
            i = y / cellnline
            j = x / cellnline
            if y % cellnline == 0 and x % cellnline == 0:
                return None
            return (i,j)
        return None
    
    def draw_lines(self, surface):
        for x in range(1, GRID_SIZE):
            pos = CELL_SIZE * x + LINE_WIDTH/2 + LINE_WIDTH * (x-1)
            pygame.draw.line(surface, LINE_COLOR, (pos, 0), (pos, SIZE), LINE_WIDTH)
            pygame.draw.line(surface, LINE_COLOR, (0, pos), (SIZE, pos), LINE_WIDTH)

class CellSprite(pygame.sprite.Sprite):
    def __init__(self, state, coords, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        self.coords = coords
        self.state = state
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(COLORS[state])
        self.rect = self.get_rect(coords) 

    def update(self):
        self.image.fill(COLORS[self.state])

    def draw(self, surface):
        # invert coordinates for drawing with x-y positions
        print "draw: ", self.coords
        surface.blit(self.image, rect)
    
    def get_rect(self, coords):
        x_pos = coords[1] * (CELL_SIZE + LINE_WIDTH)
        y_pos = coords[0] * (CELL_SIZE + LINE_WIDTH)
        return pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
