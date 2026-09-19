from common import *  # noqa
from manim import *

# Scene 23 - Safety constraints (433.02-451.48)
D = 18.46

class Scene023(SyncedScene):
    DURATION = D

    def construct(self):
        shield = VGroup(Polygon([-0.35, 0.35, 0], [0.35, 0.35, 0], [0.35, -0.08, 0],
                                [0, -0.4, 0], [-0.35, -0.08, 0],
                                stroke_color=GREEN, stroke_width=2.6,
                                fill_color=GREEN, fill_opacity=0.15),
                        polyline_check(GREEN, 0.4, sw=3).move_to([0, -0.02, 0]))
        sc = chip("SAFETY CONSTRAINTS", color=GREEN, size=21).move_to([0, 2.6, 0])
        shield.next_to(sc, LEFT, buff=0.18)
        self.play_at(0.00, FadeIn(shield), FadeIn(sc), run_time=0.6)

        # narrow corridor, head-on robots
        wallt = Rectangle(width=6.0, height=0.3, stroke_color=GRIDC,
                          stroke_width=2, fill_color=PANEL_BG2,
                          fill_opacity=0.9).move_to([0, 1.15, 0])
        wallb = wallt.copy().move_to([0, -1.15, 0])
        r1 = robot_icon(BLUE, 1.0).move_to([-2.0, 0.0, 0])
        r2 = robot_icon(ORANGE, 1.0).move_to([2.0, 0.0, 0])
        corr = VGroup(wallt, wallb, r1, r2)
        self.play_at(5.88, FadeIn(corr), run_time=0.9)

        warn = VGroup(Line([-0.35, 0.25, 0], [0.35, -0.25, 0], stroke_color=RED,
                           stroke_width=4),
                      Line([-0.35, -0.25, 0], [0.35, 0.25, 0], stroke_color=RED,
                           stroke_width=4))
        wl = chip("COLLISION RISK", color=RED, size=18).move_to([0, -1.85, 0])
        self.play_at(7.98, FadeIn(warn), FadeIn(wl), run_time=0.6)

        # slow and yield
        yield_l = Arc(radius=0.5, start_angle=-PI / 2, angle=PI,
                      stroke_color=YELLOW, stroke_width=3).move_to([-2.6, 0.0, 0])
        yield_r = Arc(radius=0.5, start_angle=PI / 2, angle=PI,
                      stroke_color=YELLOW, stroke_width=3).move_to([2.6, 0.0, 0])
        yl = chip("SLOW + YIELD", color=YELLOW, size=18).move_to([0, 1.85, 0])
        self.play_at(9.80, FadeOut(warn), FadeOut(wl), FadeIn(yield_l),
                     FadeIn(yield_r), FadeIn(yl),
                     r1.animate.shift(LEFT * 0.5), r2.animate.shift(RIGHT * 0.5),
                     run_time=0.8)

        # three-pan balance
        post = Line([0, -3.3, 0], [0, -2.5, 0], stroke_color=MUT, stroke_width=4)
        beam = Line([-2.0, -2.5, 0], [2.0, -2.5, 0], stroke_color=INK,
                    stroke_width=4)
        pivot = dot([0, -2.5, 0], r=0.06, color=INK)
        p1 = Arc(radius=0.45, start_angle=0, angle=PI, stroke_color=GREEN,
                 stroke_width=3).move_to([-2.0, -2.85, 0])
        p2 = Arc(radius=0.45, start_angle=0, angle=PI, stroke_color=TEAL,
                 stroke_width=3).move_to([0.0, -2.85, 0])
        p3 = Arc(radius=0.45, start_angle=0, angle=PI, stroke_color=YELLOW,
                 stroke_width=3).move_to([2.0, -2.85, 0])
        l1 = label("GOALS", size=15, color=GREEN).move_to(p1.get_center() + DOWN * 0.26)
        l2 = label("LOCAL", size=15, color=TEAL).move_to(p2.get_center() + DOWN * 0.26)
        l3 = label("SAFETY", size=15, color=YELLOW).move_to(p3.get_center() + DOWN * 0.26)
        bal = VGroup(post, beam, pivot, p1, p2, p3, l1, l2, l3)
        bl = label("A GOOD MULTI-AGENT SYSTEM BALANCES:", size=16, color=MUT)
        bl.move_to([0, -2.1, 0])
        self.play_at(11.54, FadeIn(bl), FadeIn(bal), run_time=0.9)

        self.wait_until(17.7)
        self.play_now(*cleanup(shield, sc, corr, yield_l, yield_r, yl, bl, bal),
                      run_time=0.6)
        self.finish()
