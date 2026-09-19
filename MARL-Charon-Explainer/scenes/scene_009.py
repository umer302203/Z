from common import *  # noqa
from manim import *

# Scene 09 - Mixed motives (141.88-149.02)
D = 7.14

class Scene009(SyncedScene):
    DURATION = D

    def construct(self):
        b1 = agent_node("A", BLUE, r=0.26).move_to([-2.0, 0.75, 0])
        b2 = agent_node("B", BLUE, r=0.26).move_to([-2.0, -0.75, 0])
        o1 = agent_node("C", ORANGE, r=0.26).move_to([2.0, 0.75, 0])
        o2 = agent_node("D", ORANGE, r=0.26).move_to([2.0, -0.75, 0])
        four = VGroup(b1, b2, o1, o2)
        self.play_at(0.00, LaggedStart(*[FadeIn(x, scale=1.4) for x in four],
                                       lag_ratio=0.15), run_time=0.7)

        link = Line(b1.get_right(), b2.get_right() + UP * 0.35, stroke_color=GREEN,
                    stroke_width=3.5)
        coop = chip("COOPERATE", color=GREEN, size=20).move_to([-2.0, 1.85, 0])
        self.play_at(3.38, Create(link), FadeIn(coop), run_time=0.6)

        cross = VGroup(
            Line(o1.get_left(), b1.get_right(), stroke_color=RED, stroke_width=2.6),
            Line(o2.get_left() + UP * 0.2, b2.get_right(), stroke_color=RED,
                 stroke_width=2.6),
            Line(o1.get_bottom() + LEFT * 0.1, b2.get_top() + RIGHT * 0.1,
                 stroke_color=RED, stroke_width=2.2).set_stroke(width=2),
        )
        comp = chip("COMPETE", color=RED, size=20).move_to([2.0, 1.85, 0])
        vs = label("VS", size=22, color=MUT).move_to([0, 0, 0])
        self.play_at(4.72, Create(cross), FadeIn(comp), FadeIn(vs), run_time=0.6)

        self.wait_until(6.30)
        self.play_now(*cleanup(four, link, coop, cross, comp, vs), run_time=0.5)
        self.finish()
