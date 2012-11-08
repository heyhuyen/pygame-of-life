from universe import *

if __name__ == "__main__":
    uni = Universe(3, 3, BLINKER)
    print "="*5 + "The Game of Life" + "="*5
    while True:
        uni.print_universe()
        if raw_input("Hit ENTER to continue>"):
            print "My life is over..."
            break
        uni.evolve()
