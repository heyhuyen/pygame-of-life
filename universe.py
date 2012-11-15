import event_manager
import pdb

class Game:
    STATE_CONFIG = -1
    STATE_RUNNING = 1
    STATE_PAUSED = 0

    def __init__(self, event_manager, cols, rows):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        self.universe = Universe(event_manager, cols, rows)
        self.state = Game.STATE_CONFIG

    def start(self):
        self.universe.set_origin([(1,0), (2,1), (0,2), (1,2), (2,2)])
        self.state = Game.STATE_PAUSED

        event = event_manager.GameStartedEvent(self)
        self.event_manager.post(event)

    def notify(self, event):
        if isinstance(event, event_manager.TickEvent):
            if self.state == Game.STATE_CONFIG:
                self.start()
            elif self.state == Game.STATE_RUNNING:
                self.universe.evolve()
        elif isinstance(event, event_manager.GamePauseEvent):
            self.state = Game.STATE_PAUSED if self.state else Game.STATE_RUNNING

#--------------------------------------------------------------------------------
class Universe:
    DELTAS = [  (-1, -1), (0, -1), (1, -1),
                (-1,  0),          (1,  0),
                (-1,  1), (0,  1), (1,  1) ]

    def __init__(self, event_manager, cols, rows):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

        self.num_cols = cols
        self.num_rows = rows
        self.live_cells = []
        self.cells = self.new_gen()

    def notify(self, event):
        if isinstance(event, event_manager.ConfigureRequest):
            self.toggle_cells(event.cell_list)

    def post_universe_changed_event(self):
        event = event_manager.UniverseChangedEvent(self.live_cells)
        self.event_manager.post(event)

    def new_gen(self):
        return [[0]*self.num_cols for i in range(0, self.num_rows)]

    def set_origin(self, live_list):
        for cell in live_list:
            self.cells[cell[0]][cell[1]] = 1
            self.live_cells.append(cell)
        self.post_universe_changed_event()

    def evolve(self):
        self.live_cells = []
        next_gen = self.new_gen()
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                next_gen[i][j] = next_cell = self.get_next_cell_state((i, j))
                if next_cell:
                    self.live_cells.append((i,j))
        if self.cells != next_gen:
            self.cells = next_gen
            self.post_universe_changed_event()

    def toggle_cells(self, cell_list):
        for cell in cell_list:
            self.toggle_state(cell)
        self.post_universe_changed_event()

    def toggle_state(self, (row, col)):
        if self.cells[row][col]:
            self.cells[row][col] = 0
            self.live_cells.remove((row,col))
        else:
            self.cells[row][col] = 1
            self.live_cells.append((row, col))

    def get_cell_state(self, (row, col)):
        # wrap-around not yet implemented
        if row in range(0, self.num_rows) and col in range(0, self.num_cols):
            return self.cells[row][col]
        return 0

    def get_cell_neighbor_states(self, (x, y)):
        neighbors = [(x+dx, y+dy) for dx, dy in Universe.DELTAS]
        return [self.get_cell_state(cell) for cell in neighbors]

    def get_next_cell_state(self, (row, col)):
        alive = self.cells[row][col]
        num_live_neighbors = sum(self.get_cell_neighbor_states((row, col)))
        if alive:
            return int(num_live_neighbors in [2,3])
        else:
            return int(num_live_neighbors == 3)

