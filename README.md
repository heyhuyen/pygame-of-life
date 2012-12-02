![alt
text](https://raw.github.com/heyhuyen/pygame-of-life/master/images/title.png)

This is an implementation of [Conway's Game of Life](http://en.wikipedia.org/wiki/Conway's_Game_of_Life) written as an exercise in learning [Python](http://www.python.org), [Pygame](http://www.pygame.org), and MVC. Written during [Hacker School](https://www.hackerschool.com/), Batch[4], Fall 2012.

### The Rules
The universe is an infinite grid of square cells, each dead or alive. A cell dies or lives on to the next generation based on the states of its 8 neighbors. For every tick in time:

- any live cell with less than 2 live neighbors dies
- any live cell with exactly 2 or 3 live neighbors continues living
- any live cell with more than 3 live neighbors dies
- any dead cell with exactly 3 live neighbors becomes alive

## Install Requirements
- [Python 2.7.3](http://www.python.org/download/releases/2.7.3/)
- [Pygame](http://www.pygame.org)
- a clone of this repo: `git clone https://github.com/heyhuyen/pygame-of-life.git`

## Playing the Game

Run `python life.py` and behold, the universe!

### Controls
1. Use the mouse to configure the universe's cells (the squares).
2. Hit the `RETURN` key to see them come to life.
3. Hit `RETURN` again to pause.
4. You can continue configuring cells while the universe is live or paused.

#### Cell Colors
- black = dead
- green = alive
- blue  = your mouse position
- red   = selected (configuring)

## The Code
MVC + Event Manager structure modeled after this [pygame tutorial](http://www.pygame.org/wiki/tut_design).

**event_manager.py** :
defines event classes and queues up event notifications to broadcast to registered listeners.

**universe.py** :
the model.
`Game` class maintains the game's state.
`Universe` class represents the universe as 2-D list of 0s and 1s, where 0 is a dead cell and 1 is a live cell, and handles logic for evolution of cells from one generation to the next.

**pygame_view.py** :
the view, which consists of a background with lines to depict a grid. Uses pygame sprites and sprite groups to render and update colored cells.

**life.py** :
the controller.
 `CPUSpinnerController` class runs the game clock.
 `InputController` class handles mouse and keyboard input.


##Todo/Extension Ideas
- add a start/splash screen
- enable player to specify universe dimensions
- provide preconfigured patterns
- go backwards in time?!?!
