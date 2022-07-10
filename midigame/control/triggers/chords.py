from ..actor import Actor, ActorEventHandler
from .. import get_midi_interface

class ChordHold(Actor):
    def __init__(self, notes):
        self.event_handler = ChordEventHandler(self)
        if not type(notes) is list:
            notes = [notes]
        self.notes = notes
        for note in notes:
            note_state = get_midi_interface().get_note(*note)
            note_state["hooks"]["NOTE_ON"] += [self.event_handler]
            note_state["hooks"]["NOTE_OFF"] += [self.event_handler]

class ChordEventHandler(ActorEventHandler):
    def __call__(self, action, event_state):
        if action == "NOTE_ON":
            if all([get_midi_interface().get_note(*note)["is_on"] for note in self.parent.notes]):
                self.parent.on_NOTE_ON(self.parent,event_state)
        elif action == "NOTE_OFF":
            self.parent.on_NOTE_OFF(self.parent,event_state)