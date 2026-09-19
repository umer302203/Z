from common import *  # noqa
from manim import *

# Scene 02 - Players become programs (19.50-25.84)
D = 6.34

class Scene002(SyncedScene):
    DURATION = D

    def construct(self):
        # small pitch icon
        p = RoundedRectangle(corner_radius=0.1, width=2.1, height=1.35,
                             stroke_color="#2ea043", stroke_width=2.5)
        p.set_fill("#0e1a12", 0.55)
        ml = Line(p.get_top() + DOWN * 0.05, p.get_bottom() + UP * 0.05,
                  stroke_color="#2ea043", stroke_width=1.6)
        cc = Circle(radius=0.22, stroke_color="#2ea043", stroke_width=1.6)
        p_g = VGroup(p, ml, cc).move_to([-4.3, 0.8, 0])
        pl = label("FOOTBALL", size=18, color=MUT).next_to(p_g, DOWN, buff=0.22)
        dots = VGroup(*[dot(p_g.get_center() + np.array([dx, dy, 0]), r=0.055,
                            color=c)
                        for dx, dy, c in [(-0.55, 0.3, BLUE), (-0.55, -0.3, BLUE),
                                          (0.55, 0.3, ORANGE), (0.55, -0.3, ORANGE),
                                          (0, 0.35, BLUE), (0, -0.35, ORANGE)]])
        self.play_at(0.00, FadeIn(p_g), FadeIn(dots), run_time=0.35)
        self.play_at(0.40, FadeIn(pl), run_time=0.30)

        # terminal panel
        term = panel(3.5, 2.5, stroke=GRIDC, fill=PANEL_BG2)
        bar = Rectangle(width=3.5, height=0.34, stroke_width=0,
                        fill_color="#1c2430", fill_opacity=1)
        bar.move_to(term.get_top() + DOWN * 0.17)
        tdots = VGroup(*[dot(bar.get_left() + RIGHT * (0.25 + 0.16 * i),
                             r=0.035, color=c)
                         for i, c in enumerate([RED, YELLOW, GREEN])])
        lines = VGroup(*[small_label(s, color=c, size=15)
                         for s, c in [("agent_01.policy()", BLUE),
                                      ("agent_02.policy()", ORANGE),
                                      ("agent_03.policy()", TEAL),
                                      ("env.step(...)  ->  reward", MUT)]])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        lines.move_to(term.get_center() + DOWN * 0.25 + LEFT * 0.1)
        term_g = VGroup(term, bar, tdots, lines).move_to([2.2, 0.15, 0])

        self.play_at(1.70, ReplacementTransform(p_g, term), run_time=0.45)
        agents_lab = small_label("AGENTS", size=18, color=MUT).move_to(pl)
        self.play_at(2.20, FadeOut(dots), Write(lines), FadeIn(bar), FadeIn(tdots),
                     ReplacementTransform(pl, agents_lab), run_time=0.55)

        # MARL title (left column, below pitch slot)
        big = label("MARL", size=92, color=BLUE).move_to([-4.3, -0.75, 0])
        ul = Line(big.get_left() + LEFT * 0.05, big.get_right() + RIGHT * 0.05,
                  stroke_color=BLUE, stroke_width=3).next_to(big, DOWN, buff=0.10)
        s1 = label("MULTI-AGENT", size=19, color=MUT)
        s2 = label("REINFORCEMENT LEARNING", size=19, color=MUT)
        s1.next_to(ul, DOWN, buff=0.12).align_to(big, LEFT)
        s2.next_to(s1, DOWN, buff=0.05).align_to(big, LEFT)
        sgroup = VGroup(s1, s2)
        title = VGroup(big, ul, sgroup)

        self.play_at(3.14, Write(big), run_time=0.70)
        self.play_at(3.90, Create(ul), FadeIn(sgroup, shift=UP * 0.1), run_time=0.45)

        self.wait_until(5.55)
        self.play_now(*cleanup(VGroup(p_g, pl), term_g, dots, title), run_time=0.55)
        self.finish()
