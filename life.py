import time
import pygame, sys
from pygame.locals import *
from pygame_view import PygameView
from universe import Game
from event_manager import *

class CPUSpinnerController:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self.keepGoing = True

    def run(self):
        while self.keepGoing:
            event = TickEvent()
            self.event_manager.post(event)
            time.sleep(0.1)

    def notify(self, event):
        if isinstance (event, QuitEvent):
            self.keepGoing = False
            sys.exit()

#--------------------------------------------------------------------------------
class InputController:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.event_manager.register_listener(self)

    def notify(self, event):
        if isinstance (event, TickEvent):
            for event in pygame.event.get():
                ev = None
                if event.type == pygame.QUIT:
                    ev = QuitEvent()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        ev = GamePauseEvent()
                elif event.type == pygame.MOUSEMOTION:
                    ev = MouseMoveEvent(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    ev = SelectStartEvent(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    ev = SelectEndEvent(event.pos)

                if ev:
                    self.event_manager.post(ev)

#--------------------------------------------------------------------------------
GRID_COLS = 20 # width
GRID_ROWS = 10 # height

def main():
    event_manager = EventManager()
    game = Game(event_manager, GRID_COLS, GRID_ROWS)
    view = PygameView(event_manager, GRID_COLS, GRID_ROWS)
    input_controller = InputController(event_manager)
    spinner = CPUSpinnerController(event_manager)
    spinner.run()

if __name__ == "__main__":
    main()
