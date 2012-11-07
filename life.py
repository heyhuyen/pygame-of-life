SIZE = 3
ORIGIN =[[0]*3, [1]*3, [0]*3]

def print_universe(gen):
    print '-' * 10
    print gen[0]
    print gen[1]
    print gen[2]

def get_cell((row,col)):
    if row in range(0,SIZE) and col in range(0,SIZE):
       return cur_gen[row][col]
    else:
        return 0

def get_neighbors((row,col)):
    x = [row - 1]*3 + [row]*2 + [row + 1]*3
    y = [col - 1, col, col + 1]*3
    y.pop(4) # remove middle index
    neighbors = zip(x,y)
    return [get_cell((row,col)) for row,col in neighbors]

def next_life((row, col)):
    living = cur_gen[row][col]
    neighbors = sum(get_neighbors((row, col)))
    if living:
        return neighbors in [2,3]
    else:
        return neighbors == 3
def new_gen():
    return [[0]*3 for i in range(0,SIZE)]

cur_gen = [[]]
next_gen = new_gen() 
if __name__ == "__main__":
    cur_gen = ORIGIN

    while True:
        raw_input("GO")
        next_gen = new_gen()
        print_universe(cur_gen) 

        for i, row in enumerate(cur_gen):
            for j, cell in enumerate(row):
                next_gen[i][j] = int(next_life((i, j)))
        cur_gen = next_gen
