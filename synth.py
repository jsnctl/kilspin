from pyo import Pattern, Fader, RCOsc, Delay, midiToHz, threading
from random import choice
import matplotlib.pyplot as plt
from IPython import display


class Synth:

    def __init__(self):
        self.amp = Fader(fadein=0.005, fadeout=0.05, mul=.15)
        self.osc = RCOsc(freq=[100, 100], mul=self.amp).out()
        self.delay = Delay(self.osc, delay=0.1, feedback=0.9).out()
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
        root = next(self.roots, 35)
        self.notes = [scaler(root) for _ in range(100)]


def scaler(root):
    scale = [0, 12, 24]
    return choice([root + val for val in scale])






