from common import *  # noqa
from manim import *

# Scene 17 - Drone coverage (325.98-347.90)
D = 21.92

class Scene017(SyncedScene):
    DURATION = D

    def construct(self):
        area = Rectangle(width=7.2, height=4.8, stroke_color=GRIDC,
                         stroke_width=2.5, fill_color=PANEL_BG2,
                         fill_opacity=0.7)
        d1 = drone_icon(TEAL, 1.1).move_to([-2.2, 1.2, 0])
        d2 = drone_icon(TEAL, 1.1).move_to([0.4, -0.6, 0])
        d3 = drone_icon(TEAL, 1.1).move_to([2.4, 1.5, 0])
        drs = VGroup(d1, d2, d3)
        self.play_at(0.00, FadeIn(area), LaggedStart(*[FadeIn(d, scale=1.3)
                                                       for d in drs],
                                                      lag_ratio=0.2),
                     run_time=0.9)

        loop1 = DashedVMobject(
            Ellipse(width=2.6, height=1.7, stroke_color=TEAL, stroke_width=2)
            .move_to([-1.2, 0.5, 0]), num_dashes=22)
        loop2 = DashedVMobject(
            Ellipse(width=2.6, height=1.7, stroke_color=TEAL, stroke_width=2)
            .move_to([-0.4, 0.1, 0]), num_dashes=22)
        self.play_at(4.96, Create(loop1), Create(loop2), run_time=1.0)

        rl = chip("RESCAN", color=RED, size=19).move_to([-0.8, 1.75, 0])
        flash = Ellipse(width=2.0, height=1.2, stroke_color=RED, stroke_width=3,
                        fill_color=RED, fill_opacity=0.15).move_to([-0.8, 0.3, 0])
        self.play_at(7.14, FadeIn(flash), FadeIn(rl), run_time=0.5)
        self.play_at(7.70, flash.animate.set_opacity(0.05), run_time=0.5)

        grid = mini_grid(-3.4, -2.2, 8, 6, cell=0.78, color="#1a2230", sw=1.4)
        zone_cols = [BLUE, TEAL, PURPLE]
        zones = VGroup()
        for i in range(3):
            z = Rectangle(width=2.28, height=4.42, stroke_width=0,
                          fill_color=zone_cols[i], fill_opacity=0.10)
            z.move_to([-2.28 + i * 2.32, 0.01, 0])
            zones.add(z)
        self.play_at(9.62, FadeOut(loop1), FadeOut(loop2), FadeOut(flash),
                     FadeOut(rl), FadeIn(grid), FadeIn(zones), run_time=0.9)

        cov = chip("COVERAGE UP", color=GREEN, size=20).move_to([-4.6, 2.6, 0])
        self.play_at(11.58, FadeIn(cov), run_time=0.5)

        target = dot([1.7, -0.9, 0], r=0.12, color=RED)
        ping = Circle(radius=0.3, color=RED, stroke_width=2.5).move_to(target)
        tg = label("TARGET", size=15, color=RED).next_to(target, DOWN, buff=0.14)
        self.play_at(17.24, FadeIn(target), FadeIn(ping), FadeIn(tg), run_time=0.5)
        self.play_at(17.85,
                     d1.animate.move_to([1.0, -0.3, 0]),
                     d2.animate.move_to([1.35, -1.35, 0]),
                     d3.animate.move_to([2.2, -0.45, 0]),
                     run_time=1.2)

        self.wait_until(20.9)
        self.play_now(*cleanup(area, drs, grid, zones, cov, target, ping, tg),
                      run_time=0.6)
        self.finish()
