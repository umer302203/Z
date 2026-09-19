from common import *  # noqa
from manim import *

# Scene 31 - Exploration and safety (629.86-678.34)
D = 48.48

class Scene031(SyncedScene):
    DURATION = D

    def construct(self):
        ep = panel(4.6, 3.3, stroke=BLUE).move_to([-2.6, 0.5, 0])
        xp = panel(4.6, 3.3, stroke=TEAL).move_to([2.6, 0.5, 0])
        el = chip("EXPLORE", color=BLUE, size=21).move_to([-2.6, 1.75, 0])
        xl = chip("EXPLOIT", color=TEAL, size=21).move_to([2.6, 1.75, 0])
        base = VGroup(ep, xp, el, xl)
        self.play_at(0.00, FadeIn(base), run_time=0.9)

        # explore: dotted new paths
        new_paths = VGroup(
            DashedLine([-4.3, -0.4, 0], [-0.9, 0.6, 0], dash_length=0.1,
                       stroke_color=BLUE, stroke_width=2.4),
            DashedLine([-4.3, -0.4, 0], [-2.0, -0.9, 0], dash_length=0.1,
                       stroke_color=BLUE, stroke_width=2.4),
            DashedLine([-0.9, 0.6, 0], [-0.9, -0.6, 0], dash_length=0.1,
                       stroke_color=BLUE, stroke_width=2.4),
        )
        ea = agent_node("A", BLUE, r=0.2).move_to([-4.3, -0.4, 0])
        nl = label("TRY NEW", size=15, color=MUT).move_to([-1.6, 0.05, 0])
        self.play_at(4.66, Create(new_paths), FadeIn(ea), FadeIn(nl),
                     run_time=0.8)

        # exploit: solid known path
        known = Line([0.9, -0.4, 0], [4.3, 0.5, 0], stroke_color=TEAL,
                     stroke_width=4)
        known_pts = VGroup(*[dot([0.9 + 0.85 * i, -0.4 + 0.225 * i, 0], r=0.07,
                                 color=TEAL) for i in range(5)])
        xa = agent_node("A", TEAL, r=0.2).move_to([0.9, -0.4, 0])
        kl = label("KNOWN GOOD", size=15, color=MUT).move_to([2.6, -0.1, 0])
        self.play_at(10.18, Create(known), FadeIn(known_pts), FadeIn(xa),
                     FadeIn(kl), run_time=0.8)

        # new route affects others
        ripple1 = Circle(radius=0.3, color=ORANGE, stroke_width=2.5).move_to(
            [-4.3, -0.4, 0])
        ripple2 = Circle(radius=0.55, color=ORANGE, stroke_width=2).move_to(
            [-4.3, -0.4, 0])
        ea2 = agent_node("A", ORANGE, r=0.2).move_to([-4.3, -0.4, 0])
        eb = agent_node("B", PURPLE, r=0.2).move_to([2.6, 0.5, 0])
        hit = Arrow(ripple2.get_right(), eb.get_left() + UL * 0.05, buff=0.08,
                    color=ORANGE, stroke_width=2.4, tip_length=0.16)
        hl = chip("ONE TRIAL AFFECTS ALL", color=ORANGE, size=18).move_to(
            [-2.6, -1.6, 0])
        self.play_at(15.08, FadeIn(ripple1), FadeIn(ripple2), FadeIn(ea2),
                     FadeIn(eb), FadeIn(hl), run_time=0.8)
        self.play_at(15.95, GrowArrow(hit), run_time=0.6)

        # team meter dips
        meter = bar_meter(3.6, 0.22, 0.8, GREEN)
        meter.move_to([2.6, -2.6, 0])
        mlab = label("TEAM RESULT", size=15, color=MUT).move_to(
            [0.4, -2.6, 0])
        meter_low = bar_meter(3.6, 0.22, 0.35, RED)
        meter_low.move_to([2.6, -2.6, 0])
        self.play_at(26.00, FadeIn(meter), FadeIn(mlab),
                     Transform(meter, meter_low), run_time=0.8)

        # safe exploration shield
        shield = DashedVMobject(Circle(radius=0.62, color=GREEN), num_dashes=16)
        shield.set_stroke(width=2.6)
        shield.move_to([-4.3, -0.4, 0])
        sl = chip("SAFE EXPLORATION", color=GREEN, size=19).move_to(
            [-2.6, 2.6, 0])
        self.play_at(31.02, FadeOut(ripple1), FadeOut(ripple2), FadeIn(shield),
                     FadeIn(sl), run_time=0.7)

        # guard chips
        g1 = chip("SIMULATION", color=BLUE, size=18).move_to([-3.9, -3.5, 0])
        g2 = chip("SAFETY LIMITS", color=YELLOW, size=18).move_to([-0.6, -3.5, 0])
        g3 = chip("HUMAN SUPERVISION", color=TEAL, size=18).move_to([3.1, -3.5, 0])
        self.play_at(38.02, FadeIn(g1), FadeIn(g2), FadeIn(g3), run_time=0.8)

        # deploy
        dep = Arrow([-0.4, 0.5, 0], [0.5, 0.5, 0], buff=0.06, color=INK,
                    stroke_width=3.4, tip_length=0.2)
        depl = chip("CAREFUL DEPLOY", color=GREEN, size=19).move_to([0.05, 2.6, 0])
        self.play_at(44.50, FadeOut(sl), GrowArrow(dep), FadeIn(depl),
                     run_time=0.8)

        self.wait_until(47.7)
        self.play_now(*cleanup(base, new_paths, ea, nl, known, known_pts, xa,
                               kl, ea2, eb, hit, hl, meter, mlab, shield, g1,
                               g2, g3, dep, depl), run_time=0.6)
        self.finish()
