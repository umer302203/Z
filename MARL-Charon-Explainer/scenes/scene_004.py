from common import *  # noqa
from manim import *

# Scene 04 - Maze to many agents (46.22-58.90)
D = 12.68

class Scene004(SyncedScene):
    DURATION = D

    def construct(self):
        x0, y0, cell = -3.55, -1.75, 0.70
        grid = mini_grid(x0, y0, 5, 5, cell=cell, color=GRIDC)
        # walls (inner segments)
        walls = VGroup(
            Line([x0 + 1 * cell, y0 + 4 * cell, 0], [x0 + 1 * cell, y0 + 3 * cell, 0],
                 stroke_color=MUT, stroke_width=3.5),
            Line([x0 + 2 * cell, y0 + 2 * cell, 0], [x0 + 3 * cell, y0 + 2 * cell, 0],
                 stroke_color=MUT, stroke_width=3.5),
            Line([x0 + 3 * cell, y0 + 3 * cell, 0], [x0 + 3 * cell, y0 + 1 * cell, 0],
                 stroke_color=MUT, stroke_width=3.5),
            Line([x0 + 1 * cell, y0 + 1 * cell, 0], [x0 + 2 * cell, y0 + 1 * cell, 0],
                 stroke_color=MUT, stroke_width=3.5),
        )
        exit_flag = flag_icon(GREEN, 0.85).move_to(
            [x0 + 4.5 * cell, y0 + 0.5 * cell, 0])
        maze = VGroup(grid, walls, exit_flag)
        ml = chip("MAZE", color=MUT, size=20).move_to([x0 + 1.75, 2.15, 0])
        self.play_at(0.00, FadeIn(maze), FadeIn(ml), run_time=0.7)

        def cellc(i, j):
            return np.array([x0 + (i + 0.5) * cell, y0 + (j + 0.5) * cell, 0])

        r1 = Circle(radius=0.13, color=BLUE, stroke_width=0,
                    fill_color=BLUE, fill_opacity=0.95).move_to(cellc(0, 4))
        r1g = VGroup(r1, dot(r1.get_center(), r=0.045, color=BG)).move_to(cellc(0, 4))
        self.play_at(0.35, FadeIn(r1g), run_time=0.35)

        # move toward wall (cell 1,3 blocked by wall between (1,4)-(1,3))
        path1 = Line(cellc(0, 4), cellc(1, 4)).points
        p_a = Line(cellc(0, 4), cellc(1, 4), stroke_width=0)
        self.play_at(2.28, MoveAlongPath(r1g, p_a), run_time=0.6)
        # wall hit at (1,4)->(1,3)
        hitpos = cellc(1, 3) + UP * (cell / 2)
        flash = Rectangle(width=cell * 0.9, height=0.06, stroke_width=0,
                          fill_color=RED, fill_opacity=0.9).move_to(hitpos)
        m1 = bubble("-1", color=RED, size=20, tail=None)
        m1.move_to(cellc(1, 4) + UP * 0.42)
        self.play_at(4.28, FadeIn(flash), run_time=0.2)
        self.play_at(4.48, FadeOut(flash), FadeIn(m1, shift=UP * 0.1),
                     Wiggle(r1g, scale_value=1.25, rotation_angle=0.06),
                     run_time=0.45)
        self.play_at(5.15, FadeOut(m1), run_time=0.3)

        # reroute: (1,4)->(2,4)->(3,4)->(3,3)... exit at (4,0): path via col 4
        p_b = Line(cellc(1, 4), cellc(2, 4), stroke_width=0)
        p_c = Line(cellc(2, 4), cellc(3, 4), stroke_width=0)
        p_d = Line(cellc(3, 4), cellc(4, 4), stroke_width=0)
        p_e = Line(cellc(4, 4), cellc(4, 0), stroke_width=0)
        self.play_at(5.45, MoveAlongPath(r1g, p_b), run_time=0.45)
        self.play_at(5.90, MoveAlongPath(r1g, p_c), run_time=0.45)
        self.play_at(6.35, MoveAlongPath(r1g, p_d), run_time=0.45)
        self.play_at(6.80, MoveAlongPath(r1g, p_e), run_time=1.0)
        m2 = bubble("+1", color=GREEN, size=20, tail=None)
        m2.next_to(exit_flag, UP, buff=0.12)
        self.play_at(7.85, FadeIn(m2, scale=1.3), run_time=0.45)

        # legend chips (right column)
        leg1 = chip("+R  EXIT", color=GREEN, size=20).move_to([4.35, 1.35, 0])
        leg2 = chip("-R  WALL", color=RED, size=20).move_to([4.35, 0.55, 0])
        self.play_at(2.55, FadeIn(leg1, shift=LEFT * 0.2), run_time=0.4)
        self.play_at(4.55, FadeIn(leg2, shift=LEFT * 0.2), run_time=0.4)

        # many agents
        r2g = VGroup(Circle(radius=0.13, color=TEAL, stroke_width=0,
                            fill_color=TEAL, fill_opacity=0.95)
                     .move_to(cellc(0, 2)),
                     dot(cellc(0, 2), r=0.045, color=BG)).move_to(cellc(0, 2))
        r3g = VGroup(Circle(radius=0.13, color=PURPLE, stroke_width=0,
                            fill_color=PURPLE, fill_opacity=0.95)
                     .move_to(cellc(2, 1)),
                     dot(cellc(2, 1), r=0.045, color=BG)).move_to(cellc(2, 1))
        self.play_at(5.86, FadeIn(r2g, scale=1.5), run_time=0.45)
        self.play_at(6.16, FadeIn(r3g, scale=1.5), run_time=0.45)

        # MARL chip + links
        mc = chip("MARL", color=BLUE, size=34).move_to([4.35, -0.75, 0])
        sub = label("MANY AGENTS, ONE WORLD", size=15, color=MUT)
        sub.next_to(mc, DOWN, buff=0.14)
        ln1 = DashedLine(r1g.get_center(), mc.get_left(),
                         dash_length=0.08, stroke_color=BLUE, stroke_width=1.8)
        ln2 = DashedLine(r2g.get_center(), mc.get_left(),
                         dash_length=0.08, stroke_color=TEAL, stroke_width=1.8)
        ln3 = DashedLine(r3g.get_center(), mc.get_bottom(),
                         dash_length=0.08, stroke_color=PURPLE, stroke_width=1.8)
        self.play_at(8.86, FadeIn(mc, scale=1.2), FadeIn(sub), run_time=0.55)
        self.play_at(9.45, Create(ln1), Create(ln2), Create(ln3), run_time=0.8)

        self.wait_until(12.05)
        self.play_now(*cleanup(maze, ml, r1g, r2g, r3g, m2, leg1, leg2, mc, sub,
                           ln1, ln2, ln3), run_time=0.55)
        self.finish()
