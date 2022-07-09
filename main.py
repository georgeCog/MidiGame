from midigame.midi.input import MidiUpdater
from midigame.midi.state import MidiState
from midigame.midi.actors.chords import Chord
from midigame.control.actions import presses_key
import time

state = MidiState()
updater = MidiUpdater(state, 1)

presses_key('w',Chord(["C","E","G"])).attatch(state)
presses_key('a',Chord(["C","E","G","A"])).attatch(state)
presses_key('d',Chord(["C","E","G","B♭"])).attatch(state)
#presses_key('d',Chord(["C","E","G","A#"])).attatch(state)

presses_key('s',Chord(["D","F","A"])).attatch(state)
presses_key('a',Chord(["D","F","A","B"])).attatch(state)
presses_key('d',Chord(["D","F","A","C"])).attatch(state)


try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    updater.close()