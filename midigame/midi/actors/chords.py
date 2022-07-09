from .. import label_to_key

class Chord:
    def __init__(self, notes):
        self.state = None

        self.notes = [label_to_key(note) for note in notes]
        self.note_active = {note:False for note in self.notes}
        self.active = False

        self.check_event = ChordCheckEvent(self)
    def attatch(self, state):
        self.detatch()
        self.state = state
        self.state.add_action(self.check_event, hooks=["press","release"], keys=self.notes)
    def detatch(self):
        #Remove hooks here
        self.state = None
    def set_note_active(self, note):
        self.note_active[note] = True
        self.update_active()
    def check_note_active(self, note):
        self.note_active[note] = any([note.is_on for note in self.state.get_notes(keys=[note], labels=False)])
        self.update_active()
    def is_active(self):
        return all(self.note_active.values())
    def update_active(self):
        now_active = self.is_active()
        if now_active > self.active:
            self.activated()
        if now_active < self.active:
            self.deactivated()
        self.active = now_active
    def activated(self):
        if self.activated_action:
            self.activated_action()
    def deactivated(self):
        if self.deactivated_action:
            self.deactivated_action()

class ChordCheckEvent:
    def __init__(self, chord):
        self.chord = chord
    def __call__(self, note):
        if note.last_action == "release":
            self.chord.check_note_active(note.key)
        elif note.last_action == "press":
            self.chord.set_note_active(note.key)
