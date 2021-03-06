import pygame
from pygame.locals import *
import event_manager
import pdb

# drawing sizes
CELL_SIZE = 20
LINE_WIDTH = 1

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
COLORS = [WHITE, RED, GREEN, BLUE]
STATE_DEAD = 0
STATE_SELECT = 1
STATE_ALIVE = 2
STATE_HOVER = 3

# use (x, y) for drawing coordinates
# use (i, j) for grid cell indices

class PygameView:

    def __init__(self, event_manager, cols, rows):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        self.num_rows = rows
        self.num_cols = cols
        screen_width = cols * CELL_SIZE + LINE_WIDTH * (cols - 1)
        screen_height = rows * CELL_SIZE + LINE_WIDTH * (rows - 1)

        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('The Game of LIFE')
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BG_COLOR)
        self.screen.blit(self.background, (0,0))
        self.draw_lines()

        self.live_sprites = pygame.sprite.RenderUpdates()
        self.selected = pygame.sprite.RenderUpdates()
        self.cursor = pygame.sprite.GroupSingle()

        pygame.display.update()

    def notify(self, event):
        if isinstance(event, event_manager.TickEvent):
            self.live_sprites.clear(self.screen, self.background)
            self.selected.clear(self.screen, self.background)
            self.cursor.clear(self.screen, self.background)

            self.live_sprites.update()
            self.selected.update()
            self.cursor.update()

            live_list = self.live_sprites.draw(self.screen)
            cursor = self.cursor.draw(self.screen)
            select_list = self.selected.draw(self.screen)

            pygame.display.update()
        elif isinstance(event, event_manager.QuitEvent):
            pygame.quit()
        elif isinstance(event, event_manager.UniverseChangedEvent):
            self.refresh_live_sprites(event.live_list)
        elif isinstance(event, event_manager.MouseMoveEvent):
            self.mouse_move(event.pos)
        elif isinstance(event, event_manager.SelectStartEvent):
            self.select_start(event.pos)
        elif isinstance(event, event_manager.SelectEndEvent):
            ev = event_manager.ConfigureRequest(self.select_end(event.pos))
            self.event_manager.post(ev)

    def refresh_live_sprites(self, live_list):
        self.live_sprites.empty()
        for cell in live_list:
            new_sprite = CellSprite(STATE_ALIVE, cell)
            new_sprite.add(self.live_sprites)

    def mouse_move(self, pos):
        sprite = self.get_cell_sprite(pos)
        if sprite:
            if len(sprite.groups()) == 0 and len(self.selected) == 0:
                sprite.state = STATE_HOVER
                sprite.add(self.cursor)
            elif self.selected not in sprite.groups() and len(self.selected) != 0:
                    sprite.add(self.selected)
                    sprite.state = STATE_SELECT
        else:
            self.cursor.empty()

    def select_start(self, pos):
        sprite = self.get_cell_sprite(pos)
        if sprite:
            sprite.state = STATE_SELECT
            sprite.add(self.selected)

    def select_end(self, pos):
        sprite = self.get_cell_sprite(pos)
        if sprite and self.selected not in sprite.groups():
            sprite.state = STATE_SELECT
            sprite.add(self.selected)
        cell_list = [cell.coords for cell in self.selected]
        self.selected.empty()
        self.cursor.empty()
        return cell_list

    def get_cell_sprite(self, (x, y)):
        if not self.screen.get_rect().collidepoint((x,y)):
            return None
        for line in self.lines:
            if line.collidepoint((x, y)):
                return None

        for live_cell in self.live_sprites:
            if live_cell.rect.collidepoint((x, y)):
                return live_cell
        for selected_cell in self.selected:
            if selected_cell.rect.collidepoint((x, y)):
                return selected_cell

        cell_plus_line = (CELL_SIZE + LINE_WIDTH)
        coords = (y / cell_plus_line, x / cell_plus_line)
        return CellSprite(STATE_DEAD, coords)

    def draw_lines(self):
        self.lines = []
        for col in range(1, self.num_cols):
            pos = CELL_SIZE * col + LINE_WIDTH/2 + LINE_WIDTH * (col - 1)
            self.lines.append(self.draw_line((pos, 0), (pos, self.screen.get_height())))

        for row in range(1, self.num_rows):
            pos = CELL_SIZE * row + LINE_WIDTH/2 + LINE_WIDTH * (row - 1)
            self.lines.append(self.draw_line((0, pos), (self.screen.get_width(), pos)))

    def draw_line(self, start, end):
        return pygame.draw.line(self.screen, LINE_COLOR, start, end, LINE_WIDTH)

#--------------------------------------------------------------------------------
class CellSprite(pygame.sprite.Sprite):
    def __init__(self, state, coords):
        pygame.sprite.Sprite.__init__(self)
        self.coords = coords
        self.state = state
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(COLORS[state])
        self.rect = self.get_rect(coords)

    def update(self):
        self.image.fill(COLORS[self.state])

    def get_rect(self, coords):
        x_pos = coords[1] * (CELL_SIZE + LINE_WIDTH)
        y_pos = coords[0] * (CELL_SIZE + LINE_WIDTH)
        return pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
