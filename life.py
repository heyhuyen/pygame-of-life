from universe import *

if __name__ == "__main__":
    uni = Universe(10, 10, GLIDER)
    print "="*5 + "The Game of Life" + "="*5
    while True:
        next_gen = new_gen(uni.height, uni.width)
        uni.print_universe()
        if raw_input("Hit ENTER to continue>"):
            print "My life is over..."
            break
        for i, row in enumerate(uni.cells):
            for j, cell in enumerate(row):
                next_gen[i][j] = uni.get_next_cell_state((i, j))
        uni.cells = next_gen
        uni.age += 1
