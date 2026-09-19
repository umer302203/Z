from common import *  # noqa
from manim import *

# Scene 05 - Policy and shared world (58.90-81.84)
D = 22.94

class Scene005(SyncedScene):
    DURATION = D

    def construct(self):
        ep = panel(3.8, 2.3, stroke=TEAL).move_to([0, -0.6, 0])
        el = label("ENVIRONMENT", size=22, color=TEAL).move_to(
            ep.get_top() + DOWN * 0.28)
        g = mini_grid(-1.45, -1.45, 5, 2, cell=0.5, color=GRIDC)
        gdots = VGroup(*[dot([x, y, 0], r=0.055, color=ORANGE)
                         for x, y in [(-1.0, -0.95), (-0.05, -1.45), (0.95, -1.2)]])
        env_g = VGroup(ep, el, g, gdots)

        A = agent_node("A", BLUE).move_to([-3.6, 0.6, 0])
        B = agent_node("B", PURPLE).move_to([3.4, 1.5, 0])
        C = agent_node("C", TEAL).move_to([3.4, -2.3, 0])
        agents = VGroup(A, B, C)

        obs1 = DashedLine(ep.get_left() + UP * 0.4, A.get_right(),
                          dash_length=0.1, stroke_color=BLUE, stroke_width=2.2)
        obs2 = DashedLine(ep.get_right() + UP * 0.5, B.get_left(),
                          dash_length=0.1, stroke_color=PURPLE, stroke_width=2.2)
        obs3 = DashedLine(ep.get_right() + DOWN * 0.6, C.get_left(),
                          dash_length=0.1, stroke_color=TEAL, stroke_width=2.2)
        obsl = arrow_label(obs1, "OBSERVES", color=MUT, size=17)

        act1 = Arrow(A.get_right(), ep.get_left() + DOWN * 0.45, buff=0.1,
                     color=BLUE, stroke_width=3, tip_length=0.2)
        act2 = Arrow(B.get_left(), ep.get_right() + UP * 0.05, buff=0.1,
                     color=PURPLE, stroke_width=3, tip_length=0.2)
        actl = arrow_label(act1, "ACTS", color=MUT, size=17)

        self.play_at(0.00, FadeIn(env_g), FadeIn(agents), run_time=0.8)
        self.play_at(0.90, Create(obs1), Create(obs2), Create(obs3),
                     FadeIn(obsl), run_time=0.9)
        self.play_at(2.60, Create(act1), Create(act2), FadeIn(actl), run_time=0.9)

        # policy card
        pc = panel(2.1, 1.15, stroke=YELLOW)
        pl = label("POLICY", size=22, color=YELLOW).move_to(pc.get_top() + DOWN * 0.28)
        rule = label("IF s THEN a", size=18, color=INK, weight="NORMAL")
        rule.move_to(pc.get_center() + DOWN * 0.22)
        policy = VGroup(pc, pl, rule).move_to([-3.9, -2.4, 0])
        parrow = Arrow(policy.get_top(), A.get_bottom() + DL * 0.05, buff=0.1,
                       color=YELLOW, stroke_width=2.4, tip_length=0.18)
        self.play_at(5.42, FadeIn(policy), GrowArrow(parrow), run_time=0.85)

        # other agents act, env changes
        self.play_at(10.28, Indicate(B, scale=1.2), Indicate(C, scale=1.2),
                     run_time=0.7)
        self.play_at(11.10, gdots[0].animate.move_to([0.4, -0.95, 0]),
                     gdots[2].animate.move_to([-0.7, -1.2, 0]), run_time=0.7)
        chip_ec = chip("ENV CHANGES", color=ORANGE, size=20).move_to([0, 2.75, 0])
        self.play_at(13.40, FadeIn(chip_ec, shift=UP * 0.15), run_time=0.5)

        # respond to other agents' decisions
        pa = Arrow(B.get_bottom(), A.get_top(), path_arc=0.5, buff=0.12,
                   color=PURPLE, stroke_width=3.2, tip_length=0.22)
        pal = label("OTHER AGENTS", size=17, color=PURPLE).move_to([1.15, 2.42, 0])
        self.play_at(19.68, GrowArrow(pa), FadeIn(pal), run_time=0.9)

        self.wait_until(22.25)
        self.play_now(*cleanup(env_g, agents, obs1, obs2, obs3, obsl, act1,
                               act2, actl, policy, parrow, chip_ec, pa, pal),
                      run_time=0.55)
        self.finish()
