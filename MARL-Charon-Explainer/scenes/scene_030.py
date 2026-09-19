from common import *  # noqa
from manim import *

# Scene 30 - Selective communication (589.88-629.86)
D = 39.98

class Scene030(SyncedScene):
    DURATION = D

    def construct(self):
        # hub with agents
        hub = Circle(radius=0.55, stroke_color=GREEN, stroke_width=2.6,
                     fill_color=GREEN, fill_opacity=0.12).move_to([0, 0.5, 0])
        hubl = label("COMMS", size=15, color=GREEN).move_to(hub)
        A = agent_node("A", BLUE, r=0.24).move_to([-3.2, 1.9, 0])
        B = agent_node("B", TEAL, r=0.24).move_to([3.2, 1.9, 0])
        C = agent_node("C", PURPLE, r=0.24).move_to([-3.2, -1.1, 0])
        Dd = agent_node("D", ORANGE, r=0.24).move_to([3.2, -1.1, 0])
        net = VGroup(hub, hubl, A, B, C, Dd)
        self.play_at(0.00, FadeIn(net), run_time=0.8)

        # all-to-all spaghetti
        pairs = [(A, B), (A, C), (A, Dd), (B, C), (B, Dd), (C, Dd),
                 (A, hub), (B, hub), (C, hub), (Dd, hub)]
        spaghetti = VGroup(*[DashedLine(a.get_center(), b.get_center(),
                                        dash_length=0.08, color=RED,
                                        stroke_width=1.6) for a, b in pairs])
        noisy = chip("NOISY + SLOW", color=RED, size=20).move_to([0, 2.6, 0])
        self.play_at(5.48, FadeOut(hubl), Create(spaghetti), FadeIn(noisy),
                     run_time=0.9)

        # what to learn
        w1 = chip("WHEN", color=BLUE, size=19).move_to([-2.2, -2.4, 0])
        w2 = chip("WHOM", color=TEAL, size=19).move_to([0.0, -2.4, 0])
        w3 = chip("WHAT", color=PURPLE, size=19).move_to([2.2, -2.4, 0])
        self.play_at(10.12, FadeIn(w1), FadeIn(w2), FadeIn(w3), run_time=0.8)

        # warehouse robot shares position only
        rob = robot_icon(BLUE, 1.0).move_to([-3.2, -1.1, 0])
        pin = dot([-3.2, -0.35, 0], r=0.09, color=BLUE)
        ring = Circle(radius=0.22, color=BLUE, stroke_width=2.2).move_to(pin)
        pl = bubble("POSITION ONLY", color=BLUE, size=15, tail=None).move_to(
            [-3.2, 0.35, 0])
        sensors = VGroup(*[Rectangle(width=0.5, height=0.12, stroke_color=MUT,
                                     stroke_width=1.6)
                           .move_to([-4.6, -0.2 - 0.22 * i, 0])
                           .set_opacity(0.35) for i in range(3)])
        sl = label("NOT EVERY READING", size=14, color=MUT).move_to(
            [-4.75, -1.75, 0])
        self.play_at(16.80, FadeIn(rob), FadeOut(C), FadeIn(pin), FadeIn(ring),
                     FadeIn(pl), FadeIn(sensors), FadeIn(sl), run_time=0.8)

        # drone shares target + confidence
        dr = drone_icon(TEAL, 1.0).move_to([3.2, -1.1, 0])
        tb = bubble("TARGET 90%", color=TEAL, size=15, tail=None).move_to(
            [3.2, 0.15, 0])
        self.play_at(22.14, FadeIn(dr), FadeOut(Dd), FadeIn(tb), run_time=0.7)

        # right time envelope
        tl = Line([-4.8, 1.9, 0], [4.8, 1.9, 0], stroke_color=GRIDC,
                  stroke_width=3)
        env1 = Rectangle(width=0.5, height=0.32, stroke_color=GREEN,
                         stroke_width=2.2, fill_color=GREEN, fill_opacity=0.25)
        env1.move_to([1.1, 1.9, 0])
        sweet = Circle(radius=0.3, color=GREEN, stroke_width=2).move_to(
            [1.1, 1.9, 0]).set_stroke(opacity=0.6)
        rtl = label("RIGHT TIME", size=15, color=GREEN).move_to([1.1, 1.45, 0])
        self.play_at(28.52, FadeIn(tl), FadeIn(env1), Create(sweet), FadeIn(rtl),
                     run_time=0.8)

        # late message
        env2 = Rectangle(width=0.5, height=0.32, stroke_color=RED,
                         stroke_width=2.2, fill_color=RED, fill_opacity=0.25)
        env2.move_to([3.9, 1.9, 0])
        dmark = polyline_cross(RED, 0.5).move_to([2.6, 1.9, 0])
        lt = label("LATE = MISSED", size=15, color=RED).move_to([3.3, 1.45, 0])
        self.play_at(33.72, FadeIn(env2), FadeIn(dmark), FadeIn(lt), run_time=0.7)

        # wrong message
        env3 = env2.copy()
        env3.move_to([-1.5, 1.9, 0]).set_stroke(PURPLE)
        wm = polyline_cross(RED, 0.45).move_to([-1.5, 1.9, 0])
        wt = label("WRONG = CHAOS", size=15, color=RED).move_to([-1.5, 1.45, 0])
        self.play_at(35.76, FadeIn(env3), FadeIn(wm), FadeIn(wt), run_time=0.7)

        # trust chips
        t1 = chip("TRUST", color=BLUE, size=17).move_to([-3.4, -3.3, 0])
        t2 = chip("VERIFY", color=TEAL, size=17).move_to([-1.2, -3.3, 0])
        t3 = chip("COST", color=YELLOW, size=17).move_to([1.0, -3.3, 0])
        self.play_at(38.0, FadeIn(t1), FadeIn(t2), FadeIn(t3), run_time=0.5)

        self.wait_until(39.2)
        self.play_now(*cleanup(net, spaghetti, noisy, w1, w2, w3, rob, pin,
                               ring, pl, sensors, sl, dr, tb, tl, env1, sweet,
                               rtl, env2, dmark, lt, env3, wm, wt, t1, t2, t3),
                      run_time=0.6)
        self.finish()
