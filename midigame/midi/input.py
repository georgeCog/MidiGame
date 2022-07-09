from rtmidi.midiutil import open_midiinput
import time

class MidiUpdater:
    def __init__(self, state, port):
        self.state = state
        # Initilize time
        self._time = time.time()
        self.state.set_time(self._time)
        # Open input port
        self.midi_in, self.port_name = open_midiinput(port)
        self.midi_in.set_callback(MidiEnvInputHandler(self))
    def close(self):
        '''Safely close IO'''
        self.midi_in.close_port()
        del self.midi_in
    def _update_time(self, deltatime):
        self._time += deltatime
        self.state.set_time(self._time)
    def _note_off(self, pitch, velocity, channel):
        self.state.update_note({"on": False, "vel": velocity}, midi_pitch=pitch)
    def _note_on(self, pitch, velocity, channel):
        self.state.update_note({"on": True, "vel": velocity}, midi_pitch=pitch)
class MidiEnvInputHandler(object):
    def __init__(self, env):
        self.env = env
    def __call__(self, event, data=None):
        (status, data0, data1), deltatime = event
        self.env._update_time(deltatime)
        action = status // 2**4
        channel = status % 2**4
        match action:
            case 0x8: 
                self.env._note_off(data0,data1,channel)
                return
            case 0x9: 
                self.env._note_on(data0,data1,channel)
                return
