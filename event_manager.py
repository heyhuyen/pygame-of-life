class Event:
    def __init__(self):
        self.name = "Generic Event"

class TickEvent(Event):
    def __init__(self):
        self.name = "Tick Event"

class QuitEvent(Event):
    def __init__(self):
        self.name = "Quit Event"

class GameStartedEvent(Event):
    def __init__(self, game):
        self.name = "Game Started Event"
        self.game = game

class GamePauseEvent(Event):
    def __init__(self):
        self.name = "Game Pause/Resume Event"

class ConfigureRequest(Event):
    def __init__(self, cell_list):
        self.name = "Configure Request"
        self.cell_list = cell_list

class UniverseChangedEvent(Event):
    def __init__(self, live_list):
        self.name = "Universe Changed Event"
        self.live_list = live_list

class MouseMoveEvent(Event):
    def __init__(self, pos):
        self.name = "Mouse Move Event"
        self.pos = pos

class SelectStartEvent(Event):
    def __init__(self, pos):
        self.name = "Select Start Event"
        self.pos = pos

class SelectEndEvent(Event):
    def __init__(self, pos):
        self.name = "Select End Event"
        self.pos = pos

#-------------------------------------------------------------------------------
class EventManager:
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def register_listener(self, listener):
        self.listeners[listener] = 1

    def post(self, event):
        if not isinstance(event, TickEvent):
            print event.name
        for listener in self.listeners:
            listener.notify(event)
