from common import *  # noqa
from manim import *

# Scene 19 - Sample efficiency and sim2real (370.00-392.90)
D = 22.90

class Scene019(SyncedScene):
    DURATION = D

    def construct(self):
        lim = chip("LIMIT 1: SAMPLE EFFICIENCY", color=ORANGE, size=22)
        lim.move_to([-3.3, 2.6, 0])
        self.play_at(0.00, FadeIn(lim), run_time=0.7)

        counter = chip("TRIALS x 1", color=INK, size=21).move_to([3.4, 2.6, 0])
        self.play_at(4.96, FadeIn(counter), run_time=0.4)
        for n, t in [("x 10", 5.45), ("x 100", 5.75), ("x 1000", 6.05)]:
            c_new = chip(f"TRIALS {n}", color=YELLOW if n == "x 1000" else INK,
                         size=21).move_to(counter)
            self.play_at(t, Transform(counter, c_new), run_time=0.28)

        # real robot: expensive + risky (top right)
        rob = robot_icon(ORANGE, 1.2).move_to([3.4, 0.9, 0])
        cost = chip("$", color=RED, size=20).move_to([4.35, 1.45, 0])
        warn = Triangle(stroke_color=RED, stroke_width=2.5,
                        fill_color=RED, fill_opacity=0.25).scale(0.2)
        warn.move_to([2.45, 1.45, 0])
        expl = label("!", size=16, color=RED).move_to(warn)
        rlab = label("REAL ROBOT", size=16, color=MUT).move_to([3.4, 0.05, 0])
        self.play_at(9.34, FadeIn(rob), FadeIn(cost), FadeIn(warn), FadeIn(expl),
                     FadeIn(rlab), run_time=0.8)

        # simulation box (bottom left)
        sim = panel(3.6, 2.0, stroke=BLUE).move_to([-4.0, -1.3, 0])
        sl_ = chip("SIM", color=BLUE, size=20).move_to(sim.get_top() + DOWN * 0.28)
        ghosts = VGroup(*[robot_icon(BLUE, 0.6).set_opacity(0.4)
                          .move_to([-4.9 + 0.65 * i, -1.6, 0]) for i in range(4)])
        simg = VGroup(sim, sl_, ghosts)
        fast = Arrow(sim.get_right() + UP * 0.3, [0.9, -1.3, 0], buff=0.08,
                     color=BLUE, stroke_width=2.6, tip_length=0.18)
        fastl = label("FAST, CHEAP", size=15, color=BLUE).move_to(
            [-1.4, -1.0, 0])
        self.play_at(13.74, FadeIn(simg), GrowArrow(fast), FadeIn(fastl),
                     run_time=0.8)

        # real world box (bottom right) + gap
        real = panel(3.6, 2.0, stroke=ORANGE).move_to([4.0, -1.3, 0])
        rlt = chip("REAL", color=ORANGE, size=20).move_to(
            real.get_top() + DOWN * 0.28)
        rrob = robot_icon(ORANGE, 0.7).move_to([4.0, -1.6, 0])
        realg = VGroup(real, rlt, rrob)
        gl = chip("SIM2REAL GAP", color=RED, size=20).move_to([0.0, -2.75, 0])
        self.play_at(18.62, FadeIn(realg), FadeIn(gl), run_time=0.9)

        self.wait_until(22.1)
        self.play_now(*cleanup(lim, counter, rob, cost, warn, expl, rlab, simg,
                               fast, fastl, realg, gl), run_time=0.6)
        self.finish()
