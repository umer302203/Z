from common import *  # noqa
from manim import *

# Scene 10 - Credit assignment (149.02-173.34)
D = 24.32

class Scene010(SyncedScene):
    DURATION = D

    def construct(self):
        q = chip("TEAM REWARD: WHO CONTRIBUTED?", color=YELLOW, size=23)
        q.move_to([0, 2.65, 0])
        self.play_at(0.00, FadeIn(q), run_time=0.8)

        box = RoundedRectangle(corner_radius=0.08, width=1.5, height=0.95,
                               stroke_color="#a07b45", stroke_width=3,
                               fill_color="#6b512e", fill_opacity=0.55)
        box.move_to([-0.9, 0.1, 0])
        xmark = VGroup(Line(UP * 0.28, DOWN * 0.28, stroke_color="#a07b45",
                            stroke_width=2.6),
                       Line(LEFT * 0.28, RIGHT * 0.28, stroke_color="#a07b45",
                            stroke_width=2.6)).move_to(box)
        boxg = VGroup(box, xmark)

        ra = robot_icon(BLUE, 0.9).move_to([-2.6, 1.35, 0])
        rb = robot_icon(PURPLE, 0.9).move_to([-2.6, -1.15, 0])
        rc = robot_icon(TEAL, 0.9).move_to([0.85, 1.35, 0])
        rd = robot_icon(MUT, 0.9).move_to([0.85, -1.15, 0])
        bots = VGroup(ra, rb, rc, rd)
        self.play_at(8.54, FadeIn(boxg), FadeIn(bots), run_time=0.9)

        flag = flag_icon(GREEN, 1.0).move_to([3.6, 0.1, 0])
        fl = label("DESTINATION", size=16, color=MUT).next_to(flag, DOWN, buff=0.15)
        banner = chip("+R TEAM", color=GREEN, size=22).move_to([3.0, 1.5, 0])
        self.play_at(12.42, FadeIn(flag), FadeIn(fl),
                     boxg.animate.move_to([2.6, 0.1, 0]),
                     bots[0].animate.move_to([-1.7, 1.35, 0]),
                     bots[1].animate.move_to([-1.7, -1.15, 0]),
                     bots[2].animate.move_to([1.75, 1.35, 0]),
                     bots[3].animate.move_to([1.75, -1.15, 0]),
                     FadeIn(banner), run_time=1.0)

        tA = chip("DIRECTION", color=BLUE, size=18).move_to([-2.9, 2.15, 0])
        aA = Arrow(tA.get_bottom(), ra.get_top(), buff=0.08, color=BLUE,
                   stroke_width=2.2, tip_length=0.15)
        self.play_at(16.08, FadeIn(tA), GrowArrow(aA), run_time=0.6)

        tB = chip("PUSH", color=PURPLE, size=18).move_to([-2.9, -1.95, 0])
        aB = Arrow(tB.get_top(), rb.get_bottom(), buff=0.08, color=PURPLE,
                   stroke_width=2.2, tip_length=0.15)
        self.play_at(19.98, FadeIn(tB), GrowArrow(aB),
                     boxg.animate.shift(RIGHT * 0.12), run_time=0.6)

        tC = chip("CLEAR WAY", color=TEAL, size=18).move_to([1.2, 2.15, 0])
        aC = Arrow(tC.get_bottom(), rc.get_top(), buff=0.08, color=TEAL,
                   stroke_width=2.2, tip_length=0.15)
        self.play_at(20.98, FadeIn(tC), GrowArrow(aC), run_time=0.6)

        idle = DashedVMobject(Circle(radius=0.42, color=MUT), num_dashes=18)
        idle.set_stroke(width=2)
        DashedCircle = idle
        DashedCircle.move_to(rd)
        dots3 = label(". . .", size=22, color=MUT).move_to(DashedCircle)
        self.play_at(22.38, rd.animate.set_opacity(0.45), FadeIn(DashedCircle),
                     FadeIn(dots3), run_time=0.6)

        self.wait_until(23.60)
        self.play_now(*cleanup(q, boxg, flag, fl, banner, bots, tA, aA, tB, aB,
                               tC, aC, DashedCircle, dots3), run_time=0.6)
        self.finish()
