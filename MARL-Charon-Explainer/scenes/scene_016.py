from common import *  # noqa
from manim import *

# Scene 16 - Warehouse robots (304.62-325.98)
D = 21.36

class Scene016(SyncedScene):
    DURATION = D

    def construct(self):
        rack_t = Rectangle(width=6.6, height=0.62, stroke_color=GRIDC,
                           stroke_width=2, fill_color=PANEL_BG2,
                           fill_opacity=0.9).move_to([0, 1.6, 0])
        rack_b = rack_t.copy().move_to([0, -1.7, 0])
        cells_t = VGroup(*[Line([-3.3 + 0.6 * i, 1.29, 0], [-3.3 + 0.6 * i, 1.91, 0],
                                stroke_color=GRIDC, stroke_width=1.4)
                           for i in range(12)])
        cells_b = cells_t.copy().move_to([0, -1.7, 0])
        dock = Rectangle(width=0.55, height=1.1, stroke_color=YELLOW,
                         stroke_width=2.4, fill_color=YELLOW,
                         fill_opacity=0.15).move_to([4.0, 0, 0])
        dl = label("DOCK", size=15, color=YELLOW).move_to(dock.get_center())
        env = VGroup(rack_t, rack_b, cells_t, cells_b, dock, dl)
        r1 = robot_icon(BLUE, 1.0).move_to([-2.2, -0.05, 0])
        r2 = robot_icon(PURPLE, 1.0).move_to([0.3, -0.05, 0])
        pk = VGroup(*[Rectangle(width=0.4, height=0.32, stroke_color=ORANGE,
                                stroke_width=2, fill_color=ORANGE,
                                fill_opacity=0.3).move_to([x, -0.05, 0])
                       for x in [-1.2, -0.6, 1.1]])
        self.play_at(0.00, FadeIn(env), FadeIn(r1), FadeIn(r2), FadeIn(pk),
                     run_time=0.9)

        carried = pk[0].copy().move_to(r1.get_center() + UP * 0.42)
        self.play_at(2.56, FadeOut(pk[0]), FadeIn(carried),
                     r1.animate.move_to([3.3, -0.05, 0]),
                     carried.animate.move_to([3.3, 0.37, 0]), run_time=1.0)
        tick = polyline_check(GREEN, 0.5).move_to([3.3, 0.85, 0])
        self.play_at(3.62, FadeIn(tick), carried.animate.set_opacity(0.15),
                     run_time=0.4)

        busy = Rectangle(width=2.6, height=0.85, stroke_color=RED,
                         stroke_width=2.2, fill_color=RED,
                         fill_opacity=0.18).move_to([0.4, 0.0, 0])
        bl = label("BUSY AISLE", size=15, color=RED).move_to([0.4, 0.0, 0])
        detour = ArcBetweenPoints([-2.2, -0.05, 0], [1.4, -0.6, 0], angle=0.8,
                                  stroke_color=BLUE, stroke_width=2.6)
        detour.add_tip(tip_length=0.18, tip_width=0.18)
        self.play_at(4.88, FadeIn(busy), FadeIn(bl), Create(detour),
                     r2.animate.move_to([1.4, -0.6, 0]), run_time=0.9)

        split1 = Arrow(r1.get_center() + DOWN * 0.3, pk[1].get_center() + UP * 0.3,
                       buff=0.1, color=GREEN, stroke_width=2.4, tip_length=0.16)
        split2 = Arrow(r2.get_center() + DOWN * 0.3, pk[2].get_center() + UP * 0.3,
                       buff=0.1, color=GREEN, stroke_width=2.4, tip_length=0.16)
        t1 = polyline_check(GREEN, 0.5).next_to(pk[1], DOWN, buff=0.12)
        t2 = polyline_check(GREEN, 0.5).next_to(pk[2], DOWN, buff=0.12)
        dl2 = chip("DIVIDE TASKS", color=GREEN, size=19).move_to([-4.3, 2.5, 0])
        self.play_at(9.02, Create(split1), Create(split2), FadeIn(t1), FadeIn(t2),
                     FadeIn(dl2), run_time=0.9)

        bolt = bolt_icon(YELLOW, 1.0).move_to([-4.35, -1.7, 0])
        bolt_bg = Circle(radius=0.3, color=YELLOW, stroke_width=2).move_to(bolt)
        conf = chip("CHARGER CONFLICT", color=RED, size=17).move_to([-4.35, -0.95, 0])
        self.play_at(11.72, FadeIn(bolt), FadeIn(bolt_bg), FadeIn(conf),
                     run_time=0.7)

        chips = VGroup(chip("NO COLLISION", color=BLUE, size=18),
                       chip("DEADLINES", color=TEAL, size=18),
                       chip("ENERGY", color=YELLOW, size=18))
        chips.arrange(RIGHT, buff=0.35).move_to([0, 2.6, 0])
        self.play_at(15.64, LaggedStart(*[FadeIn(c, shift=UP * 0.12)
                                          for c in chips], lag_ratio=0.25),
                     run_time=0.9)

        self.wait_until(20.5)
        self.play_now(*cleanup(env, r1, r2, pk, carried, tick, busy, bl, detour,
                               split1, split2, t1, t2, dl2, bolt, bolt_bg, conf,
                               chips), run_time=0.6)
        self.finish()
