from common import *  # noqa
from manim import *

# Scene 08 - Non-stationarity (118.84-141.88)
D = 23.04

class Scene008(SyncedScene):
    DURATION = D

    def construct(self):
        bg = mini_grid(-6.8, -3.9, 19, 11, cell=0.72, color="#141a22", sw=1.2)
        self.add(bg)

        def policy_card(pos, name):
            p = panel(2.5, 1.5, stroke=BLUE).move_to(pos)
            n = label(name, size=21, color=BLUE).move_to(p.get_top() + DOWN * 0.30)
            v = label("v1", size=26, color=INK).move_to(p.get_center() + DOWN * 0.25)
            return VGroup(p, n, v), v

        cardA, vA = policy_card([-2.7, -0.2, 0], "PLAYER A")
        cardB, vB = policy_card([2.7, -0.2, 0], "PLAYER B")
        pred = Arrow(cardA[0].get_right(), cardB[0].get_left(), buff=0.14,
                     color=MUT, stroke_width=3, tip_length=0.2)
        predl = label("PREDICT", size=17, color=MUT).move_to([0, 0.35, 0])
        self.play_at(0.00, FadeIn(cardA), FadeIn(cardB), GrowArrow(pred),
                     FadeIn(predl), run_time=0.9)

        crack = VGroup(Line([-3.6, -0.75, 0], [-3.25, -0.35, 0],
                            stroke_color=RED, stroke_width=3),
                       Line([-3.25, -0.35, 0], [-3.45, -0.1, 0],
                            stroke_color=RED, stroke_width=3),
                       Line([-3.45, -0.1, 0], [-3.1, 0.2, 0],
                            stroke_color=RED, stroke_width=3))
        fail = chip("CAN FAIL", color=RED, size=19).move_to([-2.7, -1.55, 0])
        self.play_at(3.66, Create(crack), FadeIn(fail), run_time=0.7)

        grid_scroll = bg.animate.shift(RIGHT * 0.72)
        ns = chip("NON-STATIONARY", color=ORANGE, size=23).move_to([0, 2.6, 0])
        self.play_at(9.06, grid_scroll, FadeIn(ns), run_time=0.9)

        vB_new = label("v2", size=26, color=INK).move_to(vB)
        self.play_at(12.38, Transform(vA, label("v2", size=26, color=INK)
                                      .move_to(vA)),
                     Transform(vB, vB_new), run_time=0.8)
        vA_new = label("v3", size=26, color=INK).move_to(vA)
        self.play_at(16.70, Transform(vB, label("v3", size=26, color=INK)
                                      .move_to(vB)),
                     Transform(vA, vA_new), run_time=0.7)

        upA = ArcBetweenPoints(cardA[0].get_top() + RIGHT * 0.3,
                               cardB[0].get_top() + LEFT * 0.3,
                               angle=-0.9, stroke_color=GREEN, stroke_width=3)
        upA.add_tip(tip_length=0.18, tip_width=0.18)
        upB = ArcBetweenPoints(cardB[0].get_top() + LEFT * 0.3,
                               cardA[0].get_top() + RIGHT * 0.3,
                               angle=-0.9, stroke_color=GREEN, stroke_width=3)
        upB.add_tip(tip_length=0.18, tip_width=0.18)
        ei = chip("EACH IMPROVES", color=GREEN, size=20).move_to([0, 1.35, 0])
        self.play_at(20.80, Create(upA), Create(upB), FadeIn(ei), run_time=0.9)

        self.wait_until(22.35)
        self.play_now(*cleanup(cardA, cardB, pred, predl, crack, fail, ns, ei,
                               upA, upB, bg), run_time=0.55)
        self.finish()
