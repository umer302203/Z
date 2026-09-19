from common import *  # noqa
from manim import *

# Scene 32 - Evaluation (678.34-721.46)
D = 43.12

class Scene032(SyncedScene):
    DURATION = D

    def construct(self):
        wl = VGroup(chip("W", color=GREEN, size=26).move_to([-1.0, 1.5, 0]),
                    chip("L", color=RED, size=26).move_to([1.0, 1.5, 0]))
        ne = chip("WIN/LOSS IS NOT ENOUGH", color=ORANGE, size=22).move_to(
            [0, 2.6, 0])
        self.play_at(0.00, FadeIn(wl), FadeIn(ne), run_time=0.8)
        self.play_at(3.0, wl.animate.set_opacity(0.25), run_time=0.5)

        # metrics dashboard
        bars = []
        names = [("TEAM REWARD", GREEN, 0.8), ("CONTRIBUTION", BLUE, 0.65),
                 ("COORDINATION", TEAL, 0.7), ("SAFETY", YELLOW, 0.9)]
        for i, (nm, col, v) in enumerate(names):
            y = 0.8 - 0.62 * i
            t = label(nm, size=16, color=MUT).move_to([-4.6, y, 0])
            bars.append((t, bar_meter(4.6, 0.2, v, col).move_to([-1.6, y, 0])))
        bars_flat = VGroup(*[m for pair in bars for m in pair])
        self.play_at(5.92, FadeIn(bars[0][0]), FadeIn(bars[0][1]),
                     FadeIn(bars[1][0]), FadeIn(bars[1][1]), run_time=1.0)
        self.play_at(10.92, FadeIn(bars[2][0]), FadeIn(bars[2][1]),
                     FadeIn(bars[3][0]), FadeIn(bars[3][1]), run_time=0.9)

        # domain chips
        tc = VGroup(chip("SPEED", color=BLUE, size=16),
                    chip("WAITING", color=TEAL, size=16),
                    chip("EMERGENCY", color=RED, size=16))
        tc.arrange(RIGHT, buff=0.28).move_to([3.4, 0.4, 0])
        tl_ = label("TRAFFIC", size=15, color=MUT).move_to([3.4, 0.85, 0])
        wc = VGroup(chip("CRASHES", color=RED, size=16),
                    chip("ENERGY", color=YELLOW, size=16))
        wc.arrange(RIGHT, buff=0.28).move_to([3.4, -1.0, 0])
        wl_ = label("WAREHOUSE", size=15, color=MUT).move_to([3.4, -0.55, 0])
        self.play_at(14.20, FadeIn(tl_), FadeIn(tc), run_time=0.9)
        self.play_at(17.46, FadeIn(wl_), FadeIn(wc), run_time=0.8)

        # fairness scene
        r1 = robot_icon(BLUE, 0.9).move_to([-4.4, -2.5, 0])
        load1 = bar_meter(1.4, 0.16, 0.95, RED).move_to([-4.4, -3.05, 0])
        r2 = robot_icon(TEAL, 0.9).move_to([-2.4, -2.5, 0])
        load2 = bar_meter(1.4, 0.16, 0.15, GREEN).move_to([-2.4, -3.05, 0])
        fl = chip("FAIRNESS", color=ORANGE, size=18).move_to([-0.6, -2.5, 0])
        flab = label("UNBALANCED WORKLOAD", size=14, color=MUT).move_to(
            [-3.4, -1.95, 0])
        self.play_at(26.10, FadeIn(r1), FadeIn(load1), FadeIn(r2), FadeIn(load2),
                     FadeIn(flab), FadeIn(fl), run_time=0.9)

        # new settings + robust
        sh = VGroup(*[Square(side_length=0.4, stroke_color=MUT, stroke_width=2)
                      .move_to([2.6 + 0.75 * i, -2.5, 0]).rotate(0.2 * i)
                      for i in range(3)])
        shl = chip("NEW SETTINGS", color=BLUE, size=18).move_to([3.4, -3.15, 0])
        self.play_at(30.96, FadeIn(sh), FadeIn(shl), run_time=0.7)

        shield = VGroup(Polygon([-0.3, 0.3, 0], [0.3, 0.3, 0], [0.3, -0.07, 0],
                                [0, -0.35, 0], [-0.3, -0.07, 0],
                                stroke_color=GREEN, stroke_width=2.4,
                                fill_color=GREEN, fill_opacity=0.15),
                        polyline_check(GREEN, 0.35, sw=3).move_to([0, -0.02, 0]))
        shield.move_to([5.6, -2.5, 0])
        rl = chip("ROBUST", color=GREEN, size=18).move_to([5.6, -3.15, 0])
        self.play_at(37.40, FadeIn(shield), FadeIn(rl), run_time=0.7)

        self.wait_until(42.3)
        self.play_now(*cleanup(wl, ne, bars_flat, tl_, tc, wl_, wc, r1, load1,
                               r2, load2, fl, flab, sh, shl, shield, rl),
                      run_time=0.6)
        self.finish()
