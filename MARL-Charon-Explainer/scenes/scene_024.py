from common import *  # noqa
from manim import *

# Scene 24 - Core idea recap (451.48-466.10)
D = 14.62

class Scene024(SyncedScene):
    DURATION = D

    def construct(self):
        q = chip("CORE IDEA?", color=YELLOW, size=24).move_to([0, 2.6, 0])
        self.play_at(0.00, FadeIn(q), run_time=0.6)

        # chain: OBSERVE -> ACT -> REWARD -> BEHAVIOR
        n1 = panel(2.5, 1.35, stroke=BLUE).move_to([-4.4, 0.4, 0])
        n1i = eye_icon(BLUE, 1.1).move_to([-4.4, 0.65, 0])
        n1l = label("OBSERVE", size=18, color=BLUE).move_to([-4.4, 0.1, 0])
        g1 = VGroup(n1, n1i, n1l)
        self.play_at(3.14, FadeIn(g1), run_time=0.6)

        n2 = panel(2.5, 1.35, stroke=PURPLE).move_to([-1.45, 0.4, 0])
        n2l = label("ACT", size=18, color=PURPLE).move_to([-1.45, 0.62, 0])
        n2s = label("POLICY", size=14, color=MUT).move_to([-1.45, 0.22, 0])
        g2 = VGroup(n2, n2l, n2s)
        a12 = Arrow(n1[0].get_right(), n2[0].get_left(), buff=0.1, color=MUT,
                    stroke_width=3, tip_length=0.2)
        self.play_at(7.38, FadeIn(g2), GrowArrow(a12), run_time=0.6)

        n3 = panel(2.5, 1.35, stroke=GREEN).move_to([1.5, 0.4, 0])
        n3t = chip("+R", color=GREEN, size=19).move_to([1.5, 0.62, 0])
        n3l = label("REWARD", size=18, color=GREEN).move_to([1.5, 0.2, 0])
        g3 = VGroup(n3, n3t, n3l)
        a23 = Arrow(n2[0].get_right(), n3[0].get_left(), buff=0.1, color=MUT,
                    stroke_width=3, tip_length=0.2)
        self.play_at(9.28, FadeIn(g3), GrowArrow(a23), run_time=0.6)

        n4 = panel(2.5, 1.35, stroke=YELLOW).move_to([4.45, 0.4, 0])
        n4l = label("BEHAVIOR", size=18, color=YELLOW).move_to([4.45, 0.55, 0])
        g4 = VGroup(n4, n4l)
        a34 = Arrow(n3[0].get_right(), n4[0].get_left(), buff=0.1, color=MUT,
                    stroke_width=3, tip_length=0.2)
        self.play_at(11.26, FadeIn(g4), GrowArrow(a34), run_time=0.5)

        coop = Line(n4[0].get_bottom() + LEFT * 0.4, [3.4, -1.5, 0],
                    stroke_color=GREEN, stroke_width=3)
        comp = Line(n4[0].get_bottom() + RIGHT * 0.4, [5.5, -1.5, 0],
                    stroke_color=RED, stroke_width=3)
        cl = chip("COOPERATION", color=GREEN, size=17).move_to([2.9, -1.85, 0])
        kl = chip("COMPETITION", color=RED, size=17).move_to([5.9, -1.85, 0])
        many = label("MANY AGENTS", size=17, color=MUT).move_to([-4.4, -1.1, 0])
        self.play_at(11.85, Create(coop), Create(comp), FadeIn(cl), FadeIn(kl),
                     FadeIn(many), run_time=0.7)

        self.wait_until(13.9)
        self.play_now(*cleanup(q, g1, g2, g3, g4, a12, a23, a34, coop, comp,
                               cl, kl, many), run_time=0.55)
        self.finish()
