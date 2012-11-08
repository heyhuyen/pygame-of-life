BLOCK = [[0]*3, [0]+[1]*2, [0]+[1]*2]
BLINKER = [[0]*3, [1]*3, [0]*3]
TOAD = [[0]*4, [0]+[1]*3, [1]*3 +[0], [0]*4]
BEACON = [[1]*2+[0]*2, [1]*2+[0]*2, [0]*2+[1]*2, [0]*2+[1]*2] 
GLIDER = [  [0]*2+[1]+[0]*7,
            [1]+[0]+[1]+[0]*7,
            [0]+[1]*2+[0]*7,
            [0]*10,
            [0]*10,
            [0]*10,
            [0]*10,
            [0]*10,
            [0]*10,
            [0]*10 ]

def new_gen(rows, cols):
    return [[0]*cols for i in range(0, rows)]

class Universe:

    def __init__(self, height, width, origin=None):
        self.width = height
        self.height = width
        self.age = 0
        if not origin:
            self.cells = new_gen(height, width)
        else:
            self.cells = origin

    def evolve(self):
        next_gen = new_gen(self.height, self.width)
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                next_gen[i][j] = self.get_next_cell_state((i,j))
        self.cells = next_gen
        self.age += 1

    def print_universe(self):
        print "Generation %d: " % self.age
        for row in self.cells:
            print row

    def get_cell_state(self, (row, col)):
        if row in range(0, self.height) and col in range(0, self.width):
           return self.cells[row][col]
        else:
            return 0

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
