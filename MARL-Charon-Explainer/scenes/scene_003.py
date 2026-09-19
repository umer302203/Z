from common import *  # noqa
from manim import *

# Scene 03 - Reinforcement learning loop (25.84-46.22)
D = 20.38

class Scene003(SyncedScene):
    DURATION = D

    def construct(self):
        # agent panel (top)
        ap = panel(3.0, 1.15, stroke=BLUE).move_to([0, 2.0, 0])
        rob = robot_icon(BLUE, 0.9).move_to(ap.get_center() + LEFT * 0.95)
        al = label("AGENT", size=26, color=BLUE).move_to(ap.get_center() + RIGHT * 0.45)
        agent_g = VGroup(ap, rob, al)

        # environment panel (bottom)
        ep = panel(4.8, 1.9, stroke=TEAL).move_to([0, -1.9, 0])
        el = label("ENVIRONMENT", size=24, color=TEAL).move_to(
            ep.get_top() + DOWN * 0.30)
        mini = mini_grid(-1.7, -2.62, 5, 2, cell=0.52, color=GRIDC)
        obs_d = VGroup(*[dot([x, y, 0], r=0.06, color=ORANGE)
                         for x, y in [(-1.18, -2.10), (-0.14, -2.62), (0.9, -2.36)]])
        env_g = VGroup(ep, el, mini, obs_d)

        self.play_at(0.00, FadeIn(agent_g, shift=DOWN * 0.2), run_time=0.6)
        self.play_at(5.56, FadeIn(env_g, shift=UP * 0.2), run_time=0.7)

        # action & observation curves
        a_path = Line([1.6, 1.42, 0], [1.6, -0.95, 0], path_arc=-0.55)
        a_arr = Arrow(a_path.get_start(), a_path.get_end(), path_arc=-0.55,
                      buff=0.0, color=ORANGE, stroke_width=3.5, tip_length=0.24)
        a_lab = label("ACTION", size=20, color=ORANGE).move_to([3.05, 0.2, 0])

        o_path = Line([-1.6, -0.95, 0], [-1.6, 1.42, 0], path_arc=-0.55)
        o_arr = Arrow(o_path.get_start(), o_path.get_end(), path_arc=-0.55,
                      buff=0.0, color=BLUE, stroke_width=3.5, tip_length=0.24)
        o_lab = label("INFORMATION", size=20, color=BLUE).move_to([-3.35, 0.2, 0])

        self.play_at(9.90, Create(o_arr), FadeIn(o_lab, shift=RIGHT * 0.2),
                     run_time=0.8)
        self.play_at(11.36, Create(a_arr), FadeIn(a_lab, shift=LEFT * 0.2),
                     run_time=0.8)

        # reward / penalty tokens
        tok_p = chip("+R", color=GREEN, size=24).move_to([-2.6, -0.45, 0])
        tok_n = chip("-R", color=RED, size=24).move_to([-2.6, -1.15, 0])
        tokn_leg = VGroup(tok_n)
        self.play_at(13.48, FadeIn(tok_p, scale=1.4), run_time=0.45)
        self.play_at(14.30, FadeIn(tok_n, scale=1.4), run_time=0.45)

        # learning pulse + chip
        lc = chip("LEARNING", color=YELLOW, size=24).move_to([4.6, 2.0, 0])
        self.play_at(16.26, FadeIn(lc, shift=LEFT * 0.2), run_time=0.45)
        flash1 = ShowPassingFlash(o_arr.copy().set_stroke(YELLOW, 5), time_width=0.5)
        flash2 = ShowPassingFlash(a_arr.copy().set_stroke(YELLOW, 5), time_width=0.5)
        self.play_at(17.00, flash1, run_time=0.7)
        self.play_at(17.75, flash2, Indicate(lc, scale=1.12), run_time=0.7)
        self.play_at(18.50, ShowPassingFlash(
            o_arr.copy().set_stroke(YELLOW, 5), time_width=0.5), run_time=0.7)

        self.wait_until(19.75)
        self.play_now(*cleanup(agent_g, env_g, o_arr, a_arr, o_lab, a_lab,
                           tok_p, tokn_leg, lc), run_time=0.55)
        self.finish()
