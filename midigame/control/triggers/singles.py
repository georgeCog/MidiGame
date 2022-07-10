from ..actor import Actor
from .. import get_midi_interface

class NoteHold(Actor):
    def __init__(self, notes):
        super().__init__()
        if not type(notes) is list:
            notes = [notes]
        for note in notes:
            note_state = get_midi_interface().get_note(*note)
            note_state["hooks"]["NOTE_ON"] += [self.event_handler]
            note_state["hooks"]["NOTE_OFF"] += [self.event_handler]
class PadHold(NoteHold):
    pass

class NoteTap(Actor):
    def __init__(self, notes):
        super().__init__()
        if not type(notes) is list:
            notes = [notes]
        for note in notes:
            note_state = get_midi_interface().get_note(*note)
            note_state["hooks"]["NOTE_ON"] += [self.event_handler]
class PadTap(NoteTap):
    pass

        
