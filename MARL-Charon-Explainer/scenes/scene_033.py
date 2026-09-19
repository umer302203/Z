from common import *  # noqa
from manim import *

# Scene 33 - Future and responsibility (721.46-779.37)
D = 57.91

class Scene033(SyncedScene):
    DURATION = D

    def construct(self):
        rail = Arc(radius=3.1, start_angle=PI * 0.15, angle=PI * 0.7,
                   stroke_color=GRIDC, stroke_width=2).move_to([0, -0.9, 0])
        fut = label("BEYOND GAMES AND SIMULATIONS", size=18, color=MUT)
        fut.move_to([0, 2.7, 0])
        self.play_at(0.00, FadeIn(rail), FadeIn(fut), run_time=0.7)

        # domain chips along the arc
        dom_specs = [("FACTORIES", 727.56, -4.4), ("VEHICLES", 728.50, -2.4),
                     ("HEALTHCARE", 729.50, -0.4), ("DISASTER", 730.50, 1.7),
                     ("ENERGY", 731.50, 3.9)]
        doms = []
        for nm, t_abs, x in dom_specs:
            c = chip(nm, color=BLUE, size=18).move_to([x, -0.35, 0])
            doms.append((t_abs - 721.46, c))
        for t, c in doms:
            self.play_at(t, FadeIn(c, scale=1.2), run_time=0.35)

        # responsibility shield
        shield = VGroup(Polygon([-0.5, 0.5, 0], [0.5, 0.5, 0], [0.5, -0.12, 0],
                                [0, -0.55, 0], [-0.5, -0.12, 0],
                                stroke_color=GREEN, stroke_width=3,
                                fill_color=GREEN, fill_opacity=0.12),
                        polyline_check(GREEN, 0.55, sw=3.5).move_to([0, -0.03, 0]))
        shield.move_to([0, -1.9, 0])
        resp = label("WITH POWER COMES RESPONSIBILITY", size=17, color=MUT)
        resp.move_to([0, -3.3, 0])
        orbit = VGroup(chip("PRIVACY", color=TEAL, size=15).move_to([-3.2, -1.4, 0]),
                       chip("SAFETY", color=BLUE, size=15).move_to([3.2, -1.4, 0]),
                       chip("FAIRNESS", color=PURPLE, size=15).move_to([-3.2, -2.5, 0]),
                       chip("HUMAN", color=YELLOW, size=15).move_to([3.2, -2.5, 0]))
        links = VGroup(*[Line(orbit[0].get_right(), shield.get_left() + UP * 0.1,
                              stroke_color=TEAL, stroke_width=1.6),
                         Line(orbit[1].get_left(), shield.get_right() + UP * 0.1,
                              stroke_color=BLUE, stroke_width=1.6),
                         Line(orbit[2].get_right(), shield.get_left() + DOWN * 0.1,
                              stroke_color=PURPLE, stroke_width=1.6),
                         Line(orbit[3].get_left(), shield.get_right() + DOWN * 0.1,
                              stroke_color=YELLOW, stroke_width=1.6)])
        self.play_at(19.16, FadeIn(shield), FadeIn(resp), run_time=0.7)
        self.play_at(19.95, LaggedStart(*[FadeIn(o, scale=1.2) for o in orbit],
                                        lag_ratio=0.15), Create(links),
                     run_time=0.9)

        # wrong goal arrow
        xmark = polyline_cross(RED, 0.8).move_to([5.6, -1.9, 0])
        fast = Arrow([2.4, -1.9, 0], xmark.get_left() + LEFT * 0.1, buff=0.08,
                     color=RED, stroke_width=3.2, tip_length=0.22)
        wg = chip("WRONG GOAL = EFFICIENTLY WRONG", color=RED, size=18)
        wg.move_to([0, -3.85, 0])
        self.play_at(25.38, GrowArrow(fast), FadeIn(xmark), FadeIn(wg),
                     run_time=0.9)

        # the fix chips
        f1 = chip("POLICIES", color=BLUE, size=17).move_to([-4.5, 1.9, 0])
        f2 = chip("GOALS", color=TEAL, size=17).move_to([-2.3, 1.9, 0])
        f3 = chip("FEEDBACK", color=YELLOW, size=17).move_to([-0.1, 1.9, 0])
        f4 = chip("OVERSIGHT", color=GREEN, size=17).move_to([2.2, 1.9, 0])
        hl = label("BETTER:", size=16, color=MUT).move_to([-6.0, 1.9, 0])
        self.play_at(31.60, FadeIn(hl), FadeIn(f1), FadeIn(f2), FadeIn(f3),
                     FadeIn(f4), run_time=0.9)

        # intelligence + coordination merge (right side, clear of all chips)
        c1 = Circle(radius=0.7, stroke_color=BLUE, stroke_width=3)
        c1.move_to([5.0, 1.35, 0])
        c1l = label("INTELLIGENCE", size=12, color=BLUE).move_to(c1)
        c2 = Circle(radius=0.7, stroke_color=GREEN, stroke_width=3)
        c2.move_to([6.35, 1.35, 0])
        c2l = label("COORDINATION", size=12, color=GREEN).move_to(c2)
        self.play_at(37.44, Create(c1), Create(c2), FadeIn(c1l), FadeIn(c2l),
                     run_time=0.9)
        self.play_at(38.50, c1.animate.move_to([5.68, 1.35, 0]),
                     c2.animate.move_to([5.68, 1.35, 0]),
                     c1l.animate.move_to([5.6, 1.48, 0]).set_opacity(0.0),
                     c2l.animate.move_to([5.75, 1.22, 0]), run_time=0.8)
        merged = label("INTELLIGENCE INCLUDES COORDINATION", size=15, color=MUT)
        merged.move_to([5.6, 0.42, 0])
        self.play_at(39.35, FadeIn(merged), run_time=0.6)

        # final question
        fq = chip("SMART FIRST, OR RESPONSIBLE FIRST?", color=YELLOW, size=22)
        fq.move_to([0, 2.6, 0])
        self.play_at(50.08, FadeIn(fq, scale=1.1), run_time=0.9)
        self.play_at(52.0, Indicate(fq, scale=1.06), run_time=0.8)

        # fade to black
        black = Rectangle(width=16, height=10, stroke_width=0, fill_color="#000000",
                          fill_opacity=0.0)
        self.add(black)
        self.play_at(56.6, black.animate.set_opacity(1.0), run_time=0.8)

        self.finish()
