from midigame.midi.input import InputInterface
from midigame.control.triggers.singles import NoteHold, PadTap

import midigame.midi.note_writer as note_writer
from midigame.midi.note_writer import note, notes, pad

import midigame.control as control

import time


midi_interface = InputInterface(1)
control.set_midi_interface(midi_interface)

note_writer.set_main_channel(0)
note_writer.set_pad_channel(9)
note_writer.set_pad_octave(1)

NoteHold(notes("C1","C2")).holds_key('w')
NoteHold(note("C#2")).holds_key('w')

PadTap(pad(1)).taps_key(' ')                # Dodge roll
PadTap(pad(5)).taps_key('a')                # Right heavy attack
PadTap(pad(3)).taps_key('b')                # Right light attack

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    midi_interface.close()