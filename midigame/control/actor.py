from json.encoder import INFINITY
from ..midi.input import ACTION_LABELS
import keyboard

def no_action_function(action):
    def func(self, _):
        print(f"Event \"{action}\" not handled by action {self}")
    return func

class Actor:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        for action in ACTION_LABELS.values():
            setattr(obj, f"on_{action}", no_action_function(action))
        return obj
    def __init__(self):
        self.event_handler = ActorEventHandler(self)
    def holds_key(self, key):
        def on(self, _):
            keyboard.press(key)
        self.on_NOTE_ON = on
        def off(self, _):
            keyboard.release(key)
        self.on_NOTE_OFF = off
        return self
    def taps_key(self, key):
        def on(self, _):
            keyboard.press_and_release(key)
        self.on_NOTE_ON = on
        return self

class ActorEventHandler(object):
    def __init__(self, parent):
        self.parent = parent
    def __call__(self, action, event_state):
        method = getattr(self.parent, f"on_{action}")
        method(self.parent, event_state)