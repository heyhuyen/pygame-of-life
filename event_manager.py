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

class RunEvent(Event):
    def __init__(self):
        self.name = "Game Run Event"

class PauseEvent(Event):
    def __init__(self):
        self.name = "Game Pause Event"

class UniverseConfiguredEvent(Event):
    def __init__(self, universe):
        self.name = "Universe Configured Event"
        self.universe = universe

class EvolveEvent(Event):
    def __init__(self, live_cells):
        self.name = "Evolve Event"
        self.live_cells = live_cells

class ConfigureRequest(Event):
    def __init__(self, cells):
        self.name = "Configure Request"
        self.cells = cells

class ConfigureEvent(Event):
    def __init__(self, live_cells):
        self.name = "Configure Event"
        self.live_cells = live_cells

class HoverEvent(Event):
    def __init__(self, pos):
        self.name = "Hover Event"
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
        self.eventQ = []

    def register_listener(self, listener):
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        if listener in self.listeners:
            del self.listeners[listener]

    def post(self, event):
        if not isinstance(event, TickEvent):
            print event.name
        for listener in self.listeners:
            listener.notify(event)
