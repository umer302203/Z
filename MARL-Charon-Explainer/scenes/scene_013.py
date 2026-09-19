from common import *  # noqa
from manim import *

# Scene 13 - Feedback gap (217.26-239.62)
D = 22.36

class Scene013(SyncedScene):
    DURATION = D

    def construct(self):
        # manager (left)
        hp = panel(3.6, 4.2, stroke=BLUE).move_to([-2.7, 0, 0])
        head = Circle(radius=0.26, stroke_color=BLUE, stroke_width=2.6,
                      fill_color=BLUE, fill_opacity=0.2).move_to([-2.7, 0.85, 0])
        body = Arc(radius=0.62, start_angle=PI, angle=-PI, stroke_color=BLUE,
                   stroke_width=2.6).move_to([-2.7, 0.18, 0])
        ml = label("HUMAN TEAM", size=18, color=BLUE).move_to([-2.7, -1.55, 0])
        mgr = VGroup(hp, head, body, ml)
        ap = panel(3.6, 4.2, stroke=TEAL).move_to([2.7, 0, 0])
        rob = robot_icon(TEAL, 1.3).move_to([2.7, 0.4, 0])
        al = label("AI AGENTS", size=18, color=TEAL).move_to([2.7, -1.55, 0])
        ag = VGroup(ap, rob, al)
        self.play_at(0.00, FadeIn(mgr), FadeIn(ag), run_time=0.8)

        b1 = bubble("GOOD PLAN", color=GREEN, size=17, tail=None).move_to([-2.7, -0.62, 0])
        b2 = bubble("GOOD TIMING", color=GREEN, size=17, tail=None).move_to([-2.7, -0.0, 0])
        b3 = bubble("WEAK COMMS", color=RED, size=17, tail=None).move_to([-2.7, 0.62, 0])
        self.play_at(2.52, LaggedStart(*[FadeIn(b, shift=UP * 0.1)
                                         for b in [b1, b2, b3]], lag_ratio=0.35),
                     run_time=1.2)

        tk1 = chip("+1", color=GREEN, size=20).move_to([2.7, 1.7, 0])
        tk2 = chip("-1", color=RED, size=20).move_to([2.7, 1.05, 0])
        ol = label("ONLY REWARD", size=17, color=MUT).move_to([2.7, -0.55, 0])
        self.play_at(8.04, FadeIn(tk1, scale=1.3), run_time=0.45)
        self.play_at(8.50, FadeIn(tk2, scale=1.3), FadeIn(ol), run_time=0.45)

        gauge_bg = Circle(radius=0.55, stroke_color=MUT, stroke_width=2.5)
        gauge_bg.move_to([0, 0.5, 0])
        needle = Line(gauge_bg.get_center(), gauge_bg.get_center() + UP * 0.42,
                      stroke_color=YELLOW, stroke_width=3)
        needle.rotate(-0.7, about_point=gauge_bg.get_center())
        gl = label("CONTRIBUTION?", size=15, color=MUT).move_to([0, -0.35, 0])
        gauge = VGroup(gauge_bg, needle, gl)
        self.play_at(10.56, FadeIn(gauge), Rotate(needle, 1.4,
                     about_point=gauge_bg.get_center()), run_time=0.8)

        slow = Arrow([-1.3, -1.9, 0], [1.3, -1.9, 0], buff=0.08, color=RED,
                     stroke_width=3, tip_length=0.2)
        sl = chip("SLOW LEARNING", color=RED, size=18).move_to([0, -2.35, 0])
        self.play_at(14.42, GrowArrow(slow), FadeIn(sl), run_time=0.7)

        path = Line([-1.3, 1.9, 0], [1.3, 1.9, 0], stroke_color=GRIDC,
                    stroke_width=3)
        flags = VGroup(*[flag_icon(GREEN, 0.65).move_to([x, 2.15, 0])
                         for x in [-0.6, 0.0, 0.6]])
        sg = chip("SUB-GOALS", color=GREEN, size=18).move_to([0, 2.65, 0])
        self.play_at(17.90, FadeOut(slow), FadeOut(sl), FadeIn(path),
                     LaggedStart(*[FadeIn(f, scale=1.2) for f in flags],
                                 lag_ratio=0.2), FadeIn(sg), run_time=0.8)

        self.wait_until(21.55)
        self.play_now(*cleanup(mgr, ag, b1, b2, b3, tk1, tk2, ol, gauge, path,
                               flags, sg), run_time=0.6)
        self.finish()
