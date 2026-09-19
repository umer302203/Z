from common import *  # noqa
from manim import *

# Scene 06 - Shared space (81.84-100.14)
D = 18.30

class Scene006(SyncedScene):
    DURATION = D

    def construct(self):
        wl = panel(4.1, 3.4, stroke=BLUE).move_to([-2.3, -0.2, 0])
        wr = panel(4.1, 3.4, stroke=TEAL).move_to([2.3, -0.2, 0])
        c1 = chip("SPACE", color=MUT, size=19).move_to([-2.4, 2.6, 0])
        c2 = chip("RESOURCES", color=MUT, size=19).move_to([-0.35, 2.6, 0])
        c3 = chip("RULES", color=MUT, size=19).move_to([1.85, 2.6, 0])
        self.play_at(0.00, FadeIn(wl), FadeIn(wr), run_time=0.7)
        self.play_at(0.80, FadeIn(c1), FadeIn(c2), FadeIn(c3), run_time=0.6)

        # warehouse aisle
        rack1 = Rectangle(width=3.3, height=0.5, stroke_color=GRIDC,
                          stroke_width=2, fill_color=PANEL_BG2,
                          fill_opacity=0.9).move_to([-2.3, 0.75, 0])
        rack2 = rack1.copy().move_to([-2.3, -1.15, 0])
        aisle = Line([-3.7, -0.2, 0], [-0.9, -0.2, 0], stroke_color=YELLOW,
                     stroke_width=4)
        al = label("ONE AISLE", size=17, color=YELLOW).move_to([-2.3, -0.62, 0])
        ra = robot_icon(BLUE, 0.8).move_to([-3.35, -0.2, 0])
        rb = robot_icon(TEAL, 0.8).move_to([-1.25, -0.2, 0])
        wh = VGroup(rack1, rack2, aisle, al, ra, rb)
        wl_tag = label("WAREHOUSE", size=18, color=BLUE).move_to([-2.3, 1.35, 0])
        self.play_at(4.80, FadeIn(wh), FadeIn(wl_tag), run_time=0.9)

        # road strip
        road = Rectangle(width=3.4, height=0.8, stroke_color=GRIDC,
                         stroke_width=2, fill_color="#182130",
                         fill_opacity=1).move_to([2.3, -0.2, 0])
        dashes = VGroup(*[Line([1.1 + 0.42 * i, -0.2, 0], [1.32 + 0.42 * i, -0.2, 0],
                               stroke_color=MUT, stroke_width=2) for i in range(6)])
        car1 = car_icon(ORANGE, 0.85).move_to([1.65, 0.02, 0])
        car2 = car_icon(ORANGE, 0.85).move_to([2.75, 0.02, 0])
        rl = label("SAME ROAD", size=17, color=MUT).move_to([2.3, -1.05, 0])
        rd = VGroup(road, dashes, car1, car2, rl)
        rd_tag = label("TRAFFIC", size=18, color=TEAL).move_to([2.3, 1.35, 0])
        self.play_at(7.78, FadeIn(rd), FadeIn(rd_tag), run_time=0.9)

        # scenario: two robots want the same charging station
        self.play_at(9.84, FadeOut(rd), FadeOut(rd_tag), run_time=0.4)
        ra2 = robot_icon(BLUE, 0.8).move_to([-3.3, -0.9, 0])
        rb2 = robot_icon(TEAL, 0.8).move_to([-1.3, 0.6, 0])
        bolt = bolt_icon(YELLOW, 1.1).move_to([-2.3, -0.2, 0])
        bolt_bg = Circle(radius=0.34, color=YELLOW, stroke_width=2).move_to(bolt)
        p1 = Arrow(ra2.get_right(), bolt_bg.get_left() + DL * 0.06, buff=0.08,
                   color=BLUE, stroke_width=2.6, tip_length=0.16)
        p2 = Arrow(rb2.get_left() + DOWN * 0.08, bolt_bg.get_top() + LEFT * 0.06,
                   buff=0.08, color=TEAL, stroke_width=2.6, tip_length=0.16)
        scen = VGroup(ra2, rb2, bolt, bolt_bg, p1, p2)
        self.play_at(10.30, FadeIn(ra2), FadeIn(rb2), FadeIn(bolt), FadeIn(bolt_bg),
                     run_time=0.5)
        self.play_at(10.85, Create(p1), Create(p2), run_time=0.7)

        # competition spark
        spark = VGroup(*[Line(bolt.get_center(),
                              bolt.get_center() + np.array([np.cos(a), np.sin(a), 0]) * 0.5,
                              stroke_color=RED, stroke_width=2.5)
                          for a in np.linspace(0, TAU, 8, endpoint=False)])
        comp = chip("COMPETITION", color=RED, size=21).move_to([2.3, -0.2, 0])
        self.play_at(12.56, FadeIn(spark), FadeIn(comp, shift=LEFT * 0.2),
                     run_time=0.7)
        self.play_at(13.30, FadeOut(spark), run_time=0.3)

        # different routes -> cooperation
        pk1 = Rectangle(width=0.42, height=0.34, stroke_color=GREEN,
                        stroke_width=2, fill_color=GREEN, fill_opacity=0.25)
        pk1.move_to([-3.3, 0.75, 0])
        pk2 = pk1.copy().move_to([-1.3, -1.35, 0])
        d1 = Arrow(ra2.get_top(), pk1.get_bottom(), buff=0.08, color=GREEN,
                   stroke_width=2.6, tip_length=0.16)
        d2 = Arrow(rb2.get_bottom(), pk2.get_top(), buff=0.08, color=GREEN,
                   stroke_width=2.6, tip_length=0.16)
        coop = chip("COOPERATION", color=GREEN, size=21).move_to([2.3, -0.2, 0])
        tick = polyline_check(GREEN, 0.8).next_to(coop, UP, buff=0.16)
        self.play_at(14.04, FadeOut(p1), FadeOut(p2), run_time=0.3)
        self.play_at(14.40, FadeIn(pk1), FadeIn(pk2), Create(d1), Create(d2),
                     run_time=0.8)
        self.play_at(16.68, FadeOut(comp), FadeIn(coop), FadeIn(tick),
                     run_time=0.55)

        self.wait_until(17.65)
        self.play_now(*cleanup(wl, wr, c1, c2, c3, wh, wl_tag, scen, coop,
                               tick, pk1, pk2, d1, d2), run_time=0.55)
        self.finish()
