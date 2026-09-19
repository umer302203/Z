from common import *
from manim import *

class T1(SyncedScene):
    DURATION = 3.0
    def construct(self):
        d = Dot()
        self.play_at(0.0, FadeIn(d), run_time=0.5)
        print("BOOK after play1:", self._t)
        self.play_at(1.0, ShowPassingFlash(d.copy().set_stroke(YELLOW,5), time_width=0.5), run_time=0.7)
        print("BOOK after flash:", self._t)
        g = VGroup(Dot(RIGHT*2), Dot(RIGHT*3))
        self.play_at(2.0, LaggedStart(*[GrowFromCenter(x) for x in g], lag_ratio=0.04), run_time=1.3)
        print("BOOK after lagged:", self._t)
        self.finish()
        print("BOOK final:", self._t)
