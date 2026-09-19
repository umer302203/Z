from common import *  # noqa
from manim import *

# Scene 11 - Reward balance (173.34-199.36)
D = 26.02

class Scene011(SyncedScene):
    DURATION = D

    def construct(self):
        pl_ = panel(4.4, 3.5, stroke=BLUE).move_to([-2.6, -0.1, 0])
        pl_t = chip("SHARED", color=BLUE, size=22).move_to([-2.6, 1.35, 0])
        pr_ = panel(4.4, 3.5, stroke=TEAL).move_to([2.6, -0.1, 0])
        pr_t = chip("INDIVIDUAL", color=TEAL, size=22).move_to([2.6, 1.35, 0])
        self.play_at(0.00, FadeIn(pl_), FadeIn(pl_t), FadeIn(pr_), FadeIn(pr_t),
                     run_time=0.8)

        def mini_bots(cx, colors):
            return VGroup(*[dot([cx - 1.35 + 0.9 * i, -0.15, 0], r=0.13,
                                color=c) for i, c in enumerate(colors)])

        sb = mini_bots(-2.6, [BLUE, PURPLE, TEAL, MUT])
        self.play_at(0.90, FadeIn(sb), run_time=0.5)
        rp = VGroup(*[chip("+R", color=GREEN, size=19).move_to(
            [x.get_x(), 0.65, 0]) for x in sb])
        self.play_at(1.45, LaggedStart(*[FadeIn(x, scale=1.3) for x in rp],
                                       lag_ratio=0.1), run_time=1.0)
        q = label("?", size=30, color=YELLOW).move_to(sb[3].get_center() + UP * 0.75)
        self.play_at(4.30, sb[3].animate.set_color(YELLOW), FadeIn(q),
                     run_time=0.6)

        ib = mini_bots(2.6, [BLUE, PURPLE, TEAL, MUT])
        self.play_at(5.26, FadeIn(ib), run_time=0.5)
        irp = chip("+R", color=GREEN, size=19).move_to([ib[3].get_x(), 0.65, 0])
        miss = label("DIRECTION MISSED", size=15, color=MUT).move_to(
            [2.6, -1.0, 0])
        self.play_at(5.80, FadeIn(irp),
                     *[x.animate.set_opacity(0.35) for x in ib[:3]],
                     FadeIn(miss), run_time=0.8)

        # balance scale (below panels, centered)
        post = Line([0, -3.75, 0], [0, -2.95, 0], stroke_color=MUT, stroke_width=4)
        beam = Line([-1.2, -2.95, 0], [1.2, -2.95, 0], stroke_color=INK,
                    stroke_width=4)
        pivot = dot([0, -2.95, 0], r=0.06, color=INK)
        pan_l = Arc(radius=0.5, start_angle=0, angle=PI, stroke_color=GREEN,
                    stroke_width=3).move_to([-1.2, -3.35, 0])
        pan_r = Arc(radius=0.5, start_angle=0, angle=PI, stroke_color=TEAL,
                    stroke_width=3).move_to([1.2, -3.35, 0])
        lt = label("TEAM", size=17, color=GREEN).move_to(pan_l.get_center() + DOWN * 0.28)
        rt_ = label("LOCAL", size=17, color=TEAL).move_to(pan_r.get_center() + DOWN * 0.28)
        scale = VGroup(post, beam, pivot, pan_l, pan_r, lt, rt_)
        sl_ = chip("BOTH REWARDS", color=INK, size=20).move_to([0, -2.3, 0])
        self.play_at(11.24, FadeOut(q), FadeIn(scale), FadeIn(sl_), run_time=0.8)

        ts = chip("TEAM SUCCESS", color=GREEN, size=19).move_to([-4.2, 2.35, 0])
        self.play_at(15.58, beam.animate.rotate(-0.16, about_point=[0, -2.95, 0]),
                     pan_l.animate.shift(UP * 0.24), pan_r.animate.shift(DOWN * 0.24),
                     lt.animate.shift(UP * 0.24), rt_.animate.shift(DOWN * 0.24),
                     FadeIn(ts), run_time=0.6)
        ls_ = chip("LOCAL ACTION", color=TEAL, size=19).move_to([4.2, 2.35, 0])
        self.play_at(18.06, beam.animate.rotate(0.28, about_point=[0, -2.95, 0]),
                     pan_l.animate.shift(DOWN * 0.44), pan_r.animate.shift(UP * 0.44),
                     lt.animate.shift(DOWN * 0.44), rt_.animate.shift(UP * 0.44),
                     FadeIn(ls_), run_time=0.6)

        selfish = chip("SELFISH", color=RED, size=18).move_to([-1.3, 2.35, 0])
        lost = chip("LOST ROLE", color=RED, size=18).move_to([1.3, 2.35, 0])
        warn = label("UNBALANCED:", size=17, color=MUT).move_to([-3.35, 2.35, 0])
        self.play_at(23.50, FadeOut(ts), FadeOut(ls_), FadeIn(warn), FadeIn(selfish),
                     FadeIn(lost), run_time=0.7)

        self.wait_until(25.25)
        self.play_now(*cleanup(pl_, pl_t, pr_, pr_t, sb, rp, ib, irp, miss,
                               scale, sl_, warn, selfish, lost), run_time=0.6)
        self.finish()
