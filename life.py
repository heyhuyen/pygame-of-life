import time
import pygame, sys
from pygame.locals import *
from event_manager import *
from universe import *
from pygame_view import PygameView

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
                        ev = RunEvent()
                    elif event.key == pygame.K_SPACE:
                        ev = PauseEvent()
                elif event.type == pygame.MOUSEMOTION:
                    ev = HoverEvent(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    ev = SelectStartEvent(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    ev = SelectEndEvent(event.pos)
                if ev:
                    self.event_manager.post(ev)
GRID_WIDTH = 10
GRID_HEIGHT = 5

def main():
    event_manager = EventManager()
    game = Game(event_manager, GRID_WIDTH, GRID_HEIGHT)
    spinner = CPUSpinnerController(event_manager)
    input_c = InputController(event_manager)
    view = PygameView(event_manager, GRID_WIDTH, GRID_HEIGHT)
    spinner.run()

if __name__ == "__main__":
    main()

