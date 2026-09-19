from common import *  # noqa
from manim import *

# Scene 12 - Delayed reward (199.36-217.26)
D = 17.90

class Scene012(SyncedScene):
    DURATION = D

    def construct(self):
        tl = Line([-5.6, -0.6, 0], [5.6, -0.6, 0], stroke_color=GRIDC,
                  stroke_width=5)
        ticks = VGroup(*[Line([x, -0.75, 0], [x, -0.45, 0], stroke_color=GRIDC,
                              stroke_width=2) for x in np.linspace(-5, 5, 11)])
        now = label("NOW", size=18, color=BLUE).move_to([-3.0, -1.15, 0])
        nmark = Line([-3.0, -0.35, 0], [-3.0, -0.85, 0], stroke_color=BLUE,
                     stroke_width=3)
        dr = drone_icon(TEAL, 1.1).move_to([-3.0, 0.15, 0])
        self.play_at(0.00, FadeIn(tl), FadeIn(ticks), FadeIn(now), FadeIn(nmark),
                     FadeIn(dr), run_time=0.8)

        an = chip("ACTION NOW", color=TEAL, size=20).move_to([-3.0, 1.15, 0])
        self.play_at(0.90, FadeIn(an), dr.animate.shift(UP * 0.18),
                     run_time=0.5)
        self.play_at(1.45, dr.animate.shift(DOWN * 0.18), run_time=0.4)

        path = Line([-3.0, 0.15, 0], [4.4, 0.15, 0], stroke_width=0)
        fl = flag_icon(GREEN, 1.1).move_to([4.4, 0.42, 0])
        t10 = chip("+10 MIN", color=ORANGE, size=20).move_to([4.35, -1.15, 0])
        self.play_at(6.70, MoveAlongPath(dr, path), run_time=1.2)
        self.play_at(8.00, FadeIn(fl), FadeIn(t10), run_time=0.6)

        qs = VGroup(*[label("?", size=26, color=YELLOW).move_to(
            [x, 0.75, 0]) for x in [-1.2, 0.6, 2.4]])
        self.play_at(11.00, LaggedStart(*[FadeIn(x, scale=1.4) for x in qs],
                                        lag_ratio=0.2), run_time=0.8)

        tc = chip("TEMPORAL CREDIT ASSIGNMENT", color=YELLOW, size=20)
        tc.move_to([-1.5, 1.85, 0])
        back = Arrow([4.4, -0.15, 0], [-3.0, -0.15, 0], buff=0.1, color=YELLOW,
                     stroke_width=2.4, tip_length=0.2)
        self.play_at(15.18, FadeIn(tc), Create(back), run_time=0.9)

        self.wait_until(17.15)
        self.play_now(*cleanup(tl, ticks, now, nmark, dr, an, fl, t10, qs, tc,
                               back), run_time=0.6)
        self.finish()
