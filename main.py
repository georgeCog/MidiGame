from midigame.midi.input import InputInterface
from midigame.control.triggers.singles import NoteHold, NoteTap
from midigame.control.triggers.chords import ChordHold

import midigame.midi.note_writer as note_writer
from midigame.midi.note_writer import note, notes, pad

import midigame.control as control

import time


midi_interface = InputInterface(1)
control.set_midi_interface(midi_interface)

note_writer.set_main_channel(0)
note_writer.set_pad_channel(9)
note_writer.set_pad_octave(1)

ChordHold(notes("G1","C2","E2")).holds_key("w") # Forward
ChordHold(notes("G1","B1","D2")).holds_key("a") # Left
ChordHold(notes("A1","C2","F2")).holds_key("d") # Right
ChordHold(notes("G1","B♭2","E2")).holds_key("d") # Back

NoteHold(note("C4")).holds_key(' ') # Dodge/Run
NoteTap(note("C0")).taps_key('q') # Lock on

ChordHold(notes("C3","G3")).taps_key("p") # Light attack
ChordHold(notes("C3","E3")).holds_key("l") # Heavy attack



try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    midi_interface.close()