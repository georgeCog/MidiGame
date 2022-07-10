from . import NUM_KEYS
import re

import sys

_default_channel = 0

_pad_octave = 0
_pad_channel = 0

def adj_octave(octave):
    return octave + 2

def set_main_channel(new_channel):
    global _default_channel
    _default_channel = new_channel

def set_pad_channel(new_channel):
    global _pad_channel
    _pad_channel = new_channel
def set_pad_octave(new_octave):
    global _pad_octave
    _pad_octave = adj_octave(new_octave)

KEY_INDICIES = {
    "C" : 0,
    "D" : 2,
    "E" : 4,
    "F" : 5,
    "G" : 7,
    "A" : 9,
    "B" : 11
}

def note(string):
    match = re.search(r"^(?P<letter>[CDEFGAB])(?P<mod>[#♭])?(?P<octave>[-\d]{1,2})$", string)
    letter = match.group('letter')
    mod = match.group('mod')
    octave = int(match.group('octave'))
    base_key = KEY_INDICIES[letter]
    if not mod is None:
        match mod:
            case "#":
                base_key += 1
            case "♭":
                base_key -= 1
    base_key %= NUM_KEYS
    octave = adj_octave(octave)
    return (_default_channel, octave, base_key)

def notes(*strings):
    return [note(string) for string in strings]

def pad(number):
    key = number - 1
    return(_pad_channel,_pad_octave,key)
