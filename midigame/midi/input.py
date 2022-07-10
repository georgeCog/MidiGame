from . import NUM_KEYS, NUM_OCTAVES, NUM_CHANNELS

from rtmidi.midiutil import open_midiinput
import time

class InputInterface:
    def __init__(self, port):
        # Initilize time
        self._time = time.time()
        # Initlilize state
        self.state = [[[ {
            "last_action_time": 0,
            "latest_action": "UNKNOWN",
            "latest_velocity": 0,
            "is_on": False,
            "hooks": {action:[] for action in list(ACTION_LABELS.values()) + ["ALL"]}
        } for _ in range(NUM_KEYS)] for _ in range(NUM_OCTAVES)] for _ in range(NUM_CHANNELS)]
        # Open input port
        self.midi_in, self.port_name = open_midiinput(port)
        self.midi_in.set_callback(InputInterfaceEventHandler(self))
    def close(self):
        '''Safely close IO'''
        self.midi_in.close_port()
        del self.midi_in
    def _update_time(self, deltatime):
        self._time += deltatime
    def get_note(self, channel, octave, key):
        return self.state[channel][octave][key]
    def all_notes(self):
        return [self.get_note(channel, octave, key) for channel in range(NUM_CHANNELS) for octave in range(NUM_OCTAVES) for key in range(NUM_KEYS)]
    def update(self, updater):
        updater(self.state)

class InputInterfaceEventHandler(object):
    def __init__(self, env):
        self.env = env
    def __call__(self, event, data=None):
        data, deltatime = event
        self.env._update_time(deltatime)
        updater = get_midi_updater(data)
        self.env.update(updater)

ACTION_LABELS = {
    0x9: "NOTE_ON",
    0x8: "NOTE_OFF",
    0xA: "KEY_PRESSURE"
}

def get_midi_updater(data):
    status, data1, data2 = data
    action = ACTION_LABELS.get(status // 2**4, "UNKNOWN")
    channel = status % 2**4
    if action == "NOTE_OFF" or action == "NOTE_ON":
        key = data1 % NUM_KEYS
        octave = data1 // NUM_KEYS
        print(channel,octave,key)
        updated_data = {
            "last_action_time" : time.time(),
            "action" : action,
            "velocity" : data2,
            "is_on" : action == "NOTE_ON"
        }
        def update_func(state):
            note_state = state[channel][octave][key]
            note_state.update(updated_data)
            for hooked_action in  note_state["hooks"][action] +  note_state["hooks"]["ALL"]:
                hooked_action(action,note_state)
        updater = update_func
    else:
        print(f"Midi action {action}[{status // 2**4}] recieved and unhandled.")
        updater = lambda state : None
    return updater


