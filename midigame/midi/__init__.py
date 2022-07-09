OCTAVE_SIZE = 12
MIDI_KEY_LABELS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
MIDI_KEY_LABELS_FLAT = ["C","D♭","D","E♭","E","F","G♭","G","A♭","A","B♭","B"]
MIDI_KEY_INDEXES = {MIDI_KEY_LABELS[index]:index for index in range(OCTAVE_SIZE)}
MIDI_KEY_INDEXES.update({MIDI_KEY_LABELS_FLAT[index]:index for index in range(OCTAVE_SIZE)})

if len(MIDI_KEY_LABELS) != OCTAVE_SIZE:
    print("WARNING: Octave size and number of note labels do not match!")

MIDI_OCTAVE_LABELS = list(range(-2,9))
MIDI_OCTAVE_INDEXES = {MIDI_OCTAVE_LABELS[index]:index for index in range(len(MIDI_OCTAVE_LABELS))}
NUM_OCTAVES = len(MIDI_OCTAVE_LABELS)

def midi_pitch_to_key_octave(midi_pitch):
    key = midi_pitch % OCTAVE_SIZE
    octave = midi_pitch // OCTAVE_SIZE
    return key, octave

def key_to_label(key):
    return MIDI_KEY_LABELS[key]
def label_to_key(label):
    return MIDI_KEY_INDEXES[label]

def octave_to_label(octave):
    return MIDI_OCTAVE_LABELS[octave]
def label_to_octave(label):
    return MIDI_OCTAVE_INDEXES[label]