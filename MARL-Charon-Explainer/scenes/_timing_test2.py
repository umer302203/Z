from common import *
from manim import *

class W1(SyncedScene):
    def construct(self):
        d = Dot()
        self.add(d)
        self.wait(0.5)
        self.play(FadeOut(d), run_time=0.5)
        self.wait(0.3)
