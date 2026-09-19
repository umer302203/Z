from common import *  # noqa
from manim import *

# Scene 28 - Roles and rewards (525.74-547.86)
D = 22.12

class Scene028(SyncedScene):
    DURATION = D

    def construct(self):
        cA = chip("A: SHARE INFO", color=BLUE, size=20).move_to([-4.6, 1.3, 0])
        cB = chip("B: PLAN ROUTE", color=TEAL, size=20).move_to([0.0, 1.3, 0])
        cC = chip("C: EXECUTE", color=PURPLE, size=20).move_to([4.6, 1.3, 0])
        a1 = Arrow(cA.get_right(), cB.get_left(), buff=0.1, color=MUT,
                   stroke_width=3, tip_length=0.2)
        a2 = Arrow(cB.get_right(), cC.get_left(), buff=0.1, color=MUT,
                   stroke_width=3, tip_length=0.2)
        self.play_at(0.00, FadeIn(cA), run_time=0.3)
        self.play_at(0.35, FadeIn(cB), GrowArrow(a1), run_time=0.3)
        self.play_at(0.70, FadeIn(cC), GrowArrow(a2), run_time=0.3)

        ring = RoundedRectangle(corner_radius=0.35, width=11.6, height=1.25,
                                stroke_color=GREEN, stroke_width=2.5)
        ring.move_to([0, 1.3, 0]).set_stroke(opacity=0.001)
        role = chip("EVERY ROLE SUPPORTS THE TEAM", color=GREEN, size=19)
        role.move_to([0, 2.5, 0])
        self.play_at(5.16, Create(ring), FadeIn(role), run_time=0.7)

        # richer rewards
        base = chip("FINAL OBJECTIVE", color=MUT, size=19).move_to([-4.2, -0.9, 0])
        plus = label("+", size=24, color=INK).move_to([-2.6, -0.9, 0])
        r1 = chip("INFO +", color=BLUE, size=18).move_to([-1.3, -0.9, 0])
        r2 = chip("NO CRASH +", color=TEAL, size=18).move_to([0.6, -0.9, 0])
        r3 = chip("TIMING +", color=YELLOW, size=18).move_to([2.6, -0.9, 0])
        rl = label("REWARDS BEYOND THE GOAL", size=16, color=MUT).move_to(
            [0, -1.75, 0])
        self.play_at(13.66, FadeIn(base), FadeIn(plus), FadeIn(r1), FadeIn(r2),
                     FadeIn(r3), FadeIn(rl), run_time=0.9)

        # team efficiency meter
        meter = bar_meter(4.4, 0.22, 0.0, GREEN)
        meter.move_to([0, -2.6, 0])
        mlab = label("TEAM EFFICIENCY", size=15, color=MUT).move_to(
            [-3.2, -2.6, 0])
        mfull = bar_meter(4.4, 0.22, 0.85, GREEN)
        mfull.move_to([0, -2.6, 0])
        self.play_at(19.0, FadeIn(meter), FadeIn(mlab),
                     Transform(meter, mfull), run_time=0.8)

        self.wait_until(21.3)
        self.play_now(*cleanup(cA, cB, cC, a1, a2, ring, role, base, plus, r1,
                               r2, r3, rl, meter, mlab), run_time=0.6)
        self.finish()
