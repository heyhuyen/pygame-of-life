import event_manager
import pdb

class Game:
    STATE_CONFIG = 'configuring'
    STATE_RUNNING = 'running'
    STATE_PAUSED = 'paused'

    def __init__(self, event_manager, width, height):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self.universe = Universe(event_manager, width, height)
        self.state = Game.STATE_CONFIG

    def start(self):
        # get configuration
        self.universe.configure([(1,0), (2,1), (0,2), (1,2), (2,2)])
        self.state = Game.STATE_PAUSED
        event = event_manager.GameStartedEvent(self)
        self.event_manager.post(event)

    def notify(self, event):
        if isinstance(event, event_manager.TickEvent):
            if self.state == Game.STATE_CONFIG:
                self.start()
            elif self.state == Game.STATE_RUNNING:
                self.universe.evolve()
                ev = event_manager.EvolveEvent(self.universe.live_cells)
                self.event_manager.post(ev)
        elif isinstance(event, event_manager.RunEvent):
            self.state = Game.STATE_RUNNING
        elif isinstance(event, event_manager.PauseEvent):
            self.state = Game.STATE_PAUSED

class Universe:

    def __init__(self, event_manager, width, height):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        self.width = width 
        self.height = height 
        self.age = 0
        self.live_cells = [] 
        self.cells = self.new_gen(height, width) 

    def configure(self, live_cells=None):
        if live_cells:
            for cell in live_cells:
                self.cells[cell[0]][cell[1]] = 1
                self.live_cells.append(cell)
        event = event_manager.UniverseConfiguredEvent(self)
        self.event_manager.post(event)

    def new_gen(self, rows, cols):
        self.dead_cells = [(i,j) for i in range(rows) for j in range(cols)]
        self.live_cells = []
        return [[0]*cols for i in range(0, rows)]

    def evolve(self):
        next_gen = self.new_gen(self.height, self.width)
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                next_gen[i][j] = next_cell = self.get_next_cell_state((i, j))
                if next_cell:
                    self.live_cells.append((i,j))
        self.cells = next_gen
        self.age += 1
    
    def get_live_cells(self):
        return self.live_cells

    def notify(self, event):
        if isinstance(event, event_manager.ConfigureRequest):
            for cell in event.cells:
                self.flip_cell_state(cell)
            ev = event_manager.ConfigureEvent(self.live_cells)
            self.event_manager.post(ev)

    def print_universe(self):
        print "Generation %d: " % self.age
        #print "Live Cells: ", self.live_cells
        for row in self.cells:
            print row

    def get_cell_state(self, (row, col)):
        if row in range(0, self.height) and col in range(0, self.width):
           return self.cells[row][col]
        else:
            return 0
    
    def set_cell_state(self, (row, col), state):
        self.cells[row][col] = state

    def flip_cell_state(self, (row, col)):
        #self.cells[row][col] = 0 if self.cells[row][col] else 1
        if self.cells[row][col]:
            self.cells[row][col] = 0
            self.live_cells.remove((row,col))
        else:
            self.cells[row][col] = 1
            self.live_cells.append((row, col))

    def get_cell_neighbors(self, (row, col)):
        x = [row - 1]*3 + [row]*2 + [row + 1]*3
        y = [col - 1, col, col + 1]*3
        y.pop(4) # remove middle index
        return [self.get_cell_state((row, col)) for row, col in zip(x, y)]

    def get_next_cell_state(self, (row, col)):
        living = self.cells[row][col]
        live_neighbors = sum(self.get_cell_neighbors((row, col)))
        if living:
            return int(live_neighbors in [2,3])
        else:
            return int(live_neighbors == 3)

