from common import *  # noqa
from manim import *

# Scene 21 - Reward design (405.40-412.52)
D = 7.12

class Scene021(SyncedScene):
    DURATION = D

    def construct(self):
        lim = chip("LIMIT 3: REWARD DESIGN", color=ORANGE, size=22)
        lim.move_to([-3.9, 2.6, 0])
        rob = robot_icon(BLUE, 1.2).move_to([-3.9, 0.9, 0])
        # speed dial
        dial = Circle(radius=0.5, stroke_color=MUT, stroke_width=2.5)
        dial.move_to([0.2, 0.7, 0])
        needle = Line(dial.get_center(), dial.get_center() + UP * 0.4,
                      stroke_color=ORANGE, stroke_width=3)
        needle.rotate(-1.0, about_point=dial.get_center())
        dl_ = label("SPEED", size=16, color=MUT).move_to([0.2, -0.05, 0])
        dialg = VGroup(dial, needle, dl_)
        self.play_at(0.00, FadeIn(lim), FadeIn(rob), FadeIn(dialg), run_time=0.8)

        # crank the dial -> speed
        dashes = VGroup(*[Line([-1.9 + 0.35 * i, 0.9, 0], [-2.15 + 0.35 * i, 0.9, 0],
                               stroke_color=BLUE, stroke_width=3)
                          for i in range(4)])
        self.play_at(1.00, Rotate(needle, 1.6, about_point=dial.get_center()),
                     FadeIn(dashes), rob.animate.shift(RIGHT * 1.1),
                     run_time=0.6)

        warn = chip("SAFETY IGNORED", color=RED, size=20).move_to([0.2, -1.2, 0])
        warn_tri = Triangle(stroke_color=RED, stroke_width=2.4,
                            fill_color=RED, fill_opacity=0.25).scale(0.22)
        warn_tri.next_to(warn, LEFT, buff=0.18)
        self.play_at(2.20, FadeIn(warn), FadeIn(warn_tri), run_time=0.6)

        # rebalance
        ok1 = chip("SPEED", color=BLUE, size=19).move_to([-1.1, -2.3, 0])
        plus = label("+", size=24, color=INK).move_to([0.0, -2.3, 0])
        ok2 = chip("SAFETY", color=GREEN, size=19).move_to([1.3, -2.3, 0])
        tick = polyline_check(GREEN, 0.6).next_to(ok2, RIGHT, buff=0.2)
        self.play_at(4.04, FadeOut(warn), FadeOut(warn_tri), FadeOut(dashes),
                     Rotate(needle, -0.8, about_point=dial.get_center()),
                     FadeIn(ok1), FadeIn(plus), FadeIn(ok2), FadeIn(tick),
                     run_time=0.8)

        self.wait_until(6.30)
        self.play_now(*cleanup(lim, rob, dialg, ok1, plus, ok2, tick),
                      run_time=0.5)
        self.finish()
