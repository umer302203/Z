from common import *  # noqa
from manim import *

# Scene 27 - Team game roles (505.66-525.74)
D = 20.08

class Scene027(SyncedScene):
    DURATION = D

    def construct(self):
        field = mini_grid(-4.4, -2.2, 10, 6, cell=0.78, color="#182028", sw=1.5)
        self.play_at(0.00, FadeIn(field), run_time=0.8)

        A = agent_node("A", BLUE, r=0.28).move_to([-3.6, 1.8, 0])
        B = agent_node("B", TEAL, r=0.28).move_to([-3.6, -0.2, 0])
        C = agent_node("C", PURPLE, r=0.28).move_to([-3.6, -1.7, 0])
        trio = VGroup(A, B, C)
        opp = agent_node("X", RED, r=0.3).move_to([3.8, 1.2, 0])
        fl = flag_icon(GREEN, 1.0).move_to([3.8, -1.5, 0])
        flab = label("OBJECTIVE", size=14, color=MUT).next_to(fl, DOWN, buff=0.12)
        self.play_at(2.84, FadeIn(trio), FadeIn(opp), FadeIn(fl), FadeIn(flab),
                     run_time=0.7)

        eyeA = DashedLine(A.get_right(), opp.get_left() + DOWN * 0.05,
                          dash_length=0.1, stroke_color=BLUE, stroke_width=2.2)
        eyei = eye_icon(BLUE, 0.8).move_to([-1.5, 1.62, 0])
        self.play_at(5.10, Create(eyeA), FadeIn(eyei), run_time=0.6)

        safeB = ArcBetweenPoints(B.get_right(), [2.9, -1.3, 0], angle=-0.55,
                                 stroke_color=TEAL, stroke_width=2.6)
        safeB.add_tip(tip_length=0.18, tip_width=0.18)
        slab = label("SAFE ROUTE", size=14, color=TEAL).move_to([-0.4, -0.6, 0])
        self.play_at(7.22, Create(safeB), FadeIn(slab), run_time=0.6)

        pathC = ArcBetweenPoints(C.get_right(), [3.4, -1.45, 0], angle=0.35,
                                 stroke_color=PURPLE, stroke_width=2.6)
        pathC.add_tip(tip_length=0.18, tip_width=0.18)
        self.play_at(8.88, Create(pathC), run_time=0.6)

        # independent chaos
        def dashed_arc(p0, p1, ang):
            a = ArcBetweenPoints(p0, p1, angle=ang, stroke_color=RED,
                                 stroke_width=2)
            return DashedVMobject(a, num_dashes=16).set_opacity(0.7)

        messy = VGroup(
            dashed_arc(A.get_center(), [1.5, -1.9, 0], 1.2),
            dashed_arc(B.get_center(), [0.9, 1.4, 0], -1.0),
            dashed_arc(C.get_center(), [2.2, 0.6, 0], 0.9),
        )
        qm = chip("DUPLICATION + CONFUSION", color=RED, size=19).move_to(
            [0.3, 2.6, 0])
        self.play_at(11.06, FadeOut(eyeA), FadeOut(eyei), FadeOut(safeB),
                     FadeOut(slab), FadeOut(pathC), Create(messy), FadeIn(qm),
                     run_time=0.9)

        # role-based clean paths
        clean1 = ArcBetweenPoints(A.get_right(), opp.get_bottom() + DOWN * 0.25,
                                  angle=-0.3, stroke_color=BLUE, stroke_width=2.6)
        clean1.add_tip(tip_length=0.16, tip_width=0.16)
        clean2 = ArcBetweenPoints(B.get_right(), [2.9, -1.3, 0], angle=-0.55,
                                  stroke_color=TEAL, stroke_width=2.6)
        clean2.add_tip(tip_length=0.16, tip_width=0.16)
        clean3 = ArcBetweenPoints(C.get_right(), [3.4, -1.45, 0], angle=0.35,
                                  stroke_color=PURPLE, stroke_width=2.6)
        clean3.add_tip(tip_length=0.16, tip_width=0.16)
        ok = chip("ROLES OK", color=GREEN, size=19).move_to([0.3, 2.6, 0])
        self.play_at(15.78, FadeOut(messy), FadeOut(qm), Create(clean1),
                     Create(clean2), Create(clean3), FadeIn(ok), run_time=0.9)

        self.wait_until(19.35)
        self.play_now(*cleanup(field, trio, opp, fl, flab, clean1, clean2,
                               clean3, ok), run_time=0.6)
        self.finish()
