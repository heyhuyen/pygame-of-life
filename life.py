SIZE = 10
BLOCK = [[0]*3, [0]+[1]*2, [0]+[1]*2]
BLINKER = [[0]*3, [1]*3, [0]*3]
TOAD = [[0]*4, [0]+[1]*3, [1]*3 +[0], [0]*4]
BEACON = [[1]*2+[0]*2, [1]*2+[0]*2, [0]*2+[1]*2, [0]*2+[1]*2] 
GLIDER = [  [0]*2+[1]+[0]*8,
            [1]+[0]+[1]+[0]*8,
            [0]+[1]*2+[0]*8,
            [0]*11,
            [0]*11,
            [0]*11,
            [0]*11,
            [0]*11,
            [0]*11,
            [0]*11,
            [0]*11 ]

def print_universe(gen, universe):
    print "Generation %d: " % gen
    for row in universe:
        print row[0:SIZE]

def new_gen():
    return [[0]*SIZE for i in range(0, SIZE)]

def cell_state((row, col)):
    if row in range(0, SIZE) and col in range(0, SIZE):
       return cur_gen[row][col]
    else:
        return 0

def get_neighbors((row, col)):
    x = [row - 1]*3 + [row]*2 + [row + 1]*3
    y = [col - 1, col, col + 1]*3
    y.pop(4) # remove middle index
    return [cell_state((row, col)) for row, col in zip(x, y)]

def next_state((row, col)):
    living = cur_gen[row][col]
    live_neighbors = sum(get_neighbors((row, col)))
    if living:
        return int(live_neighbors in [2,3])
    else:
        return int(live_neighbors == 3)

cur_gen = [[]]
next_gen = [[]] 

if __name__ == "__main__":
    cur_gen = GLIDER
    print "="*5 + "The Game of Life" + "="*5
    gen = 0
    while True:
        next_gen = new_gen()
        print_universe(gen, cur_gen) 
        if raw_input("Hit ENTER to continue>"):
            print "My life is over..."
            break
        for i, row in enumerate(cur_gen):
            for j, cell in enumerate(row):
                next_gen[i][j] = next_state((i, j))
        cur_gen = next_gen
        gen += 1
