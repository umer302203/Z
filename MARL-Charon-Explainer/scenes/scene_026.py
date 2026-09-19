from common import *  # noqa
from manim import *

# Scene 26 - Intelligence or coordination (487.62-505.66)
D = 18.04

class Scene026(SyncedScene):
    DURATION = D

    def construct(self):
        circ = Circle(radius=1.9, stroke_color=BLUE, stroke_width=2.5)
        circ.move_to([-3.6, 0.3, 0])
        cl = chip("ONE ENVIRONMENT", color=BLUE, size=19).move_to([-3.6, 2.6, 0])
        human_head = Circle(radius=0.22, stroke_color=ORANGE, stroke_width=2.4,
                            fill_color=ORANGE, fill_opacity=0.2)
        human_head.move_to([-4.3, 0.75, 0])
        human_body = Arc(radius=0.5, start_angle=PI, angle=-PI,
                         stroke_color=ORANGE, stroke_width=2.4)
        human_body.move_to([-4.3, 0.15, 0])
        ai1 = robot_icon(BLUE, 0.85).move_to([-2.8, 0.35, 0])
        ai2 = robot_icon(TEAL, 0.85).move_to([-3.6, -0.85, 0])
        world = VGroup(circ, cl, human_head, human_body, ai1, ai2)
        self.play_at(0.00, FadeIn(world), run_time=0.8)

        # balance scale
        post = Line([2.6, -1.9, 0], [2.6, 0.4, 0], stroke_color=MUT,
                    stroke_width=4)
        beam = Line([1.1, 0.4, 0], [4.1, 0.4, 0], stroke_color=INK,
                    stroke_width=4)
        pivot = dot([2.6, 0.4, 0], r=0.06, color=INK)
        pan_l = Arc(radius=0.6, start_angle=0, angle=PI, stroke_color=BLUE,
                    stroke_width=3).move_to([1.1, 0.0, 0])
        pan_r = Arc(radius=0.6, start_angle=0, angle=PI, stroke_color=GREEN,
                    stroke_width=3).move_to([4.1, 0.0, 0])
        lt = label("IQ", size=20, color=BLUE).move_to(pan_l.get_center() + DOWN * 0.3)
        rt_ = label("COORDINATION", size=16, color=GREEN).move_to(
            pan_r.get_center() + DOWN * 0.32)
        scale = VGroup(post, beam, pivot, pan_l, pan_r, lt, rt_)
        ql = label("WHAT MATTERS MORE?", size=17, color=MUT).move_to([2.6, 1.5, 0])
        self.play_at(3.48, FadeIn(scale), FadeIn(ql),
                     beam.animate.rotate(-0.14, about_point=[2.6, 0.4, 0]),
                     pan_l.animate.shift(UP * 0.26), pan_r.animate.shift(DOWN * 0.26),
                     lt.animate.shift(UP * 0.26), rt_.animate.shift(DOWN * 0.26),
                     run_time=0.8)

        # answer: both
        s1 = chip("SMART", color=BLUE, size=21).move_to([-1.2, -2.6, 0])
        plus = label("+", size=26, color=INK).move_to([0.0, -2.6, 0])
        s2 = chip("RESPONSIBLE", color=GREEN, size=21).move_to([2.4, -2.6, 0])
        self.play_at(11.26, FadeIn(s1), FadeIn(plus), FadeIn(s2), run_time=0.7)

        self.wait_until(17.3)
        self.play_now(*cleanup(world, scale, ql, s1, plus, s2), run_time=0.6)
        self.finish()
