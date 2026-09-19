from common import *  # noqa
from manim import *

# Scene 22 - Explainability (412.52-433.02)
D = 20.50

class Scene022(SyncedScene):
    DURATION = D

    def construct(self):
        lim = chip("LIMIT 4: EXPLAINABILITY", color=ORANGE, size=22)
        lim.move_to([-3.5, 2.6, 0])
        self.play_at(0.00, FadeIn(lim), run_time=0.7)

        agents = VGroup(*[agent_node(c, col, r=0.24)
                          for c, col in [("A", BLUE), ("B", TEAL), ("C", PURPLE)]])
        agents.arrange(RIGHT, buff=0.5).move_to([-3.3, 0.9, 0])
        tick = polyline_check(GREEN, 0.7).move_to([-3.3, 1.9, 0])
        self.play_at(0.98, FadeIn(agents), FadeIn(tick), run_time=0.6)

        # black box between agents and outcome
        bb = panel(2.0, 1.5, stroke=MUT, fill="#05070a", opacity=0.95)
        bb.move_to([0.4, 0.9, 0])
        qm = label("?", size=40, color=MUT).move_to(bb)
        ina = Arrow(agents.get_right(), bb.get_left(), buff=0.1, color=MUT,
                    stroke_width=2.6, tip_length=0.18)
        ol = label("SUCCESS", size=17, color=GREEN).move_to([3.2, 0.9, 0])
        outa = Arrow(bb.get_right(), ol.get_left() + LEFT * 0.06, buff=0.1,
                     color=MUT, stroke_width=2.6, tip_length=0.18)
        hid = label("HIDDEN PATTERN", size=15, color=MUT).move_to([0.4, -1.25, 0])
        self.play_at(2.48, FadeIn(bb), FadeIn(qm), GrowArrow(ina), FadeIn(ol),
                     GrowArrow(outa), FadeIn(hid), run_time=0.9)

        # safety critical
        shield = VGroup(Polygon([-0.4, 0.4, 0], [0.4, 0.4, 0], [0.4, -0.1, 0],
                                [0, -0.45, 0], [-0.4, -0.1, 0],
                                stroke_color=RED, stroke_width=2.6,
                                fill_color=RED, fill_opacity=0.15),
                        polyline_check(RED, 0.45, sw=3).move_to([0, -0.02, 0]))
        shield.move_to([0.4, 2.28, 0])
        sc = label("SAFETY CRITICAL", size=16, color=RED).move_to([2.7, 2.28, 0])
        self.play_at(10.12, FadeIn(shield), FadeIn(sc), run_time=0.7)

        # engineer reads the decision path
        eng_head = Circle(radius=0.2, stroke_color=TEAL, stroke_width=2.4,
                          fill_color=TEAL, fill_opacity=0.2).move_to([4.9, -1.3, 0])
        eng_body = Arc(radius=0.5, start_angle=PI, angle=-PI, stroke_color=TEAL,
                       stroke_width=2.4).move_to([4.9, -1.85, 0])
        eng = VGroup(eng_head, eng_body)
        englab = label("ENGINEERS", size=15, color=MUT).move_to([4.9, -2.45, 0])
        path1 = Arrow(bb.get_bottom(), eng_head.get_top() + LEFT * 0.4, buff=0.1,
                      color=TEAL, stroke_width=2.2, tip_length=0.16)
        why = chip("WHY THIS DECISION?", color=TEAL, size=18).move_to([1.6, -2.0, 0])
        self.play_at(14.88, FadeIn(eng), FadeIn(englab), GrowArrow(path1),
                     FadeIn(why), run_time=0.9)

        chips = VGroup(chip("COMMS RULES", color=BLUE, size=17),
                       chip("ROLE POLICY", color=TEAL, size=17),
                       chip("MONITORING", color=YELLOW, size=17))
        chips.arrange(RIGHT, buff=0.3).move_to([-0.4, -3.2, 0])
        self.play_at(17.48, LaggedStart(*[FadeIn(c, shift=UP * 0.12)
                                          for c in chips], lag_ratio=0.25),
                     run_time=0.9)

        self.wait_until(19.7)
        self.play_now(*cleanup(lim, agents, tick, bb, qm, ina, ol, outa, hid,
                               shield, sc, eng, englab, path1, why, chips),
                      run_time=0.6)
        self.finish()
