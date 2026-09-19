from common import *  # noqa
from manim import *

# Scene 18 - Centralized training, decentralized execution (347.90-370.00)
D = 22.10

class Scene018(SyncedScene):
    DURATION = D

    def construct(self):
        tp = panel(4.7, 4.1, stroke=BLUE).move_to([-2.55, 0, 0])
        tt = chip("TRAINING", color=BLUE, size=22).move_to([-2.55, 1.65, 0])
        hub = Circle(radius=0.5, color=YELLOW, stroke_width=2.6,
                     fill_color=YELLOW, fill_opacity=0.18).move_to([-2.55, 0.1, 0])
        hub_l = label("GLOBAL", size=15, color=YELLOW).move_to(hub)
        hub_l2 = label("INFO", size=15, color=YELLOW).move_to(
            hub.get_center() + DOWN * 0.24)
        a1 = agent_node("A", BLUE, r=0.24).move_to([-4.0, -1.25, 0])
        a2 = agent_node("B", PURPLE, r=0.24).move_to([-2.55, -1.5, 0])
        a3 = agent_node("C", TEAL, r=0.24).move_to([-1.1, -1.25, 0])
        tr = VGroup(tp, tt, hub, hub_l, hub_l2, a1, a2, a3)
        self.play_at(0.00, FadeIn(tr), run_time=0.9)

        l1 = Line(a1.get_top(), hub.get_center() + DL * 0.4, stroke_color=BLUE,
                  stroke_width=2.2)
        l2 = Line(a2.get_top(), hub.get_bottom(), stroke_color=PURPLE,
                  stroke_width=2.2)
        l3 = Line(a3.get_top(), hub.get_center() + DR * 0.4, stroke_color=TEAL,
                  stroke_width=2.2)
        self.play_at(5.48, Create(l1), Create(l2), Create(l3), run_time=1.0)

        ep = panel(4.7, 4.1, stroke=TEAL).move_to([2.55, 0, 0])
        et = chip("EXECUTION", color=TEAL, size=22).move_to([2.55, 1.65, 0])
        b1 = agent_node("A", BLUE, r=0.24).move_to([1.35, -0.4, 0])
        b2 = agent_node("B", PURPLE, r=0.24).move_to([2.75, -0.9, 0])
        b3 = agent_node("C", TEAL, r=0.24).move_to([3.9, -0.1, 0])
        cones = VGroup(
            Polygon(b1.get_center(), b1.get_center() + UR * 1.1,
                    b1.get_center() + UP * 1.0, stroke_color=BLUE,
                    stroke_width=1.6, fill_color=BLUE, fill_opacity=0.12),
            Polygon(b2.get_center(), b2.get_center() + UR * 1.0,
                    b2.get_center() + UL * 1.0, stroke_color=PURPLE,
                    stroke_width=1.6, fill_color=PURPLE, fill_opacity=0.12),
            Polygon(b3.get_center(), b3.get_center() + UL * 1.0,
                    b3.get_center() + UP * 1.1, stroke_color=TEAL,
                    stroke_width=1.6, fill_color=TEAL, fill_opacity=0.12),
        )
        er = VGroup(ep, et, b1, b2, b3, cones)
        self.play_at(13.68, FadeIn(er), run_time=0.9)

        # map icon in training
        mp = Rectangle(width=0.75, height=0.55, stroke_color=GREEN,
                       stroke_width=2, fill_color=GREEN, fill_opacity=0.15)
        mp.move_to([-2.55, -2.5, 0])
        mpl = label("FULL MAP", size=13, color=GREEN).next_to(mp, RIGHT, buff=0.12)
        mpl.shift(LEFT * 0.1)
        self.play_at(16.48, FadeIn(mp), FadeIn(mpl), run_time=0.6)

        # sensor icon in execution + THEN arrow
        sp = eye_icon(BLUE, 1.0).move_to([2.55, -2.5, 0])
        spl = label("OWN SENSORS", size=13, color=BLUE).next_to(sp, RIGHT, buff=0.14)
        spl.shift(LEFT * 0.05)
        then = Arrow([-0.1, 0, 0], [0.35, 0, 0], buff=0.06, color=INK,
                     stroke_width=3.4, tip_length=0.2)
        thenl = label("THEN", size=16, color=INK).move_to([0.12, 0.32, 0])
        self.play_at(19.10, FadeIn(sp), FadeIn(spl), GrowArrow(then),
                     FadeIn(thenl), run_time=0.7)

        self.wait_until(21.3)
        self.play_now(*cleanup(tr, er, l1, l2, l3, mp, mpl, sp, spl, then,
                               thenl), run_time=0.6)
        self.finish()
