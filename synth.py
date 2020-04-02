from pyo import Pattern, Fader, RCOsc, Delay, midiToHz, threading, Sine, SuperSaw
from random import choice

def scaler(root):
    scale = [0, 12, 24]
    return choice([root + val for val in scale])


class BaseSynth:

    def __init__(self):
        self.notes = None
        self.roots = None
        self.cloud = Pattern(function=self._cloud, time=0.095)
        self.progression = Pattern(function=self._progression, time=2)

    def start(self, roots):
        self.notes = [scaler(35) for _ in range(100)]
        self.roots = roots
        self.progression.play()
        self.cloud.play()

    def stop(self):
        self.progression.stop()
        self.cloud.stop()

    def _cloud(self):
        self.amp.dur = 0.1
        freq = choice(midiToHz(self.notes))
        self.osc.freq = [freq, freq * 1.003]
        self.amp.play()

    def _progression(self):
        root = next(self.roots)
        self.notes = [scaler(root) for _ in range(100)]


class Simple(BaseSynth):

    def __init__(self, delay=0.1, feedback=0.9):
        super().__init__()
        self.amp = Fader(fadein=0.005, fadeout=0.05, mul=.15)
        self.osc = RCOsc(freq=[100, 100], mul=self.amp).out()
        self.delay = Delay(self.osc, delay=delay, feedback=feedback).out()


class Fancy(BaseSynth):

    def __init__(self, delay=0.1, feedback=0.9):
        super().__init__()
        self.amp = Fader(fadein=0.5, fadeout=0.05, mul=.15)
        self.osc = SuperSaw(freq=[100, 100], mul=self.amp).out()
        self.delay = Delay(self.osc, delay=delay, feedback=feedback).out()

