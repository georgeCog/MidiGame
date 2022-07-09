from . import OCTAVE_SIZE, NUM_OCTAVES, MIDI_KEY_LABELS, MIDI_OCTAVE_LABELS, midi_pitch_to_key_octave, key_to_label, octave_to_label, label_to_key, label_to_octave

class MidiState:
    def __init__(self):
        '''Create a new set of note states indexed by octave and key'''
        self.notes = [[Note(key, octave) for octave in range(NUM_OCTAVES)] for key in range(OCTAVE_SIZE)]
        self.time = None
    def set_time(self, time):
        self.time = time
    def get_notes(self, keys=None, octaves=None, labels=True):
        if keys is None:
            keys = MIDI_KEY_LABELS
        if octaves is None:
            octaves = MIDI_OCTAVE_LABELS
        notes = []
        for key in keys:
            key_index = label_to_key(key) if labels else key
            key_notes = self.notes[key_index]
            notes += [key_notes[label_to_octave(octave) if labels else octave] for octave in octaves]
        return notes
    def update_note(self, options=None, midi_pitch=None, key=None, octave=None):
        if options is None:
            options = {}
        if not midi_pitch is None:
            key, octave = midi_pitch_to_key_octave(midi_pitch)
        self.notes[key][octave].update(**options)
    def add_action(self, action, hooks, keys=None):
        notes = self.get_notes(keys, labels=False)
        for note in notes:
            for hook in hooks:
                note.add_action(action,hook)

class Note:
    def __init__(self, key, octave):
        self.key = key
        self.octave = octave
        self.is_on = False
        self.vel = 0
        self.last_action = "none"

        self.action_hooks = {"press":[],"release":[],"velocity_change":[]}
        self.hook_queue = []
    def update(self, on=None, vel=None):
        if not on is None:
            self._modify_on(on)
        if not vel is None:
            self._modify_vel(vel)
        self._exicute_hooks()
    def add_action(self, action, hook):
        self.action_hooks[hook] += [action]
    def _activate_hook(self, hook_event):
        self.hook_queue += [hook_event]
    def _exicute_hooks(self):
        for hook_event in self.hook_queue:
            self.last_action = hook_event
            for action in self.action_hooks[hook_event]:
                action(self)
        self.hook_queue = []
    def _modify_on(self, on):
        if on > self.is_on:
            self._activate_hook("press")
        elif on < self.is_on:
            self._activate_hook("release")
        self.is_on = on
    def _modify_vel(self, vel):
        if vel != self.vel:
            self._activate_hook("velocity_change")
        self.vel = vel
    def __repr__(self):
        return str(self)
    def __str__(self):
        return f"<Note {key_to_label(self.key)}{octave_to_label(self.octave)}>"

class NoteHook:
    def __call__(self,note):
        print(f"{note} {note.last_action}")