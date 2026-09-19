from common import *  # noqa
from manim import *

# Scene 07 - Cooperation vs Competition (100.14-118.84)
D = 18.70

class Scene007(SyncedScene):
    DURATION = D

    def construct(self):
        lp = panel(5.7, 4.5, stroke=GREEN).move_to([-2.05, 0, 0])
        lc = chip("COOPERATION", color=GREEN, size=23).move_to([-2.05, 1.7, 0])
        self.play_at(0.00, FadeIn(lp), FadeIn(lc), run_time=0.7)

        # rescue drones over map regions
        regs = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.35,
                                         height=1.05, stroke_color=GRIDC,
                                         stroke_width=2, fill_color=TEAL,
                                         fill_opacity=0.12)
                        .move_to([-3.55 + 1.5 * i, -0.15, 0]) for i in range(3)])
        drs = VGroup(*[drone_icon(TEAL, 0.9).move_to(
            [-3.55 + 1.5 * i, 0.55, 0]) for i in range(3)])
        rl = label("RESCUE DRONES", size=18, color=TEAL).move_to([-2.05, 1.15, 0])
        self.play_at(2.46, FadeIn(regs), LaggedStart(*[FadeIn(d, scale=1.3)
                                                       for d in drs],
                                                      lag_ratio=0.15),
                     FadeIn(rl), run_time=0.9)

        routes = VGroup(*[DashedLine(d.get_bottom(), regs[i].get_center(),
                                     dash_length=0.09, stroke_color=TEAL,
                                     stroke_width=2.2)
                          for i, d in enumerate(drs)])
        ol = label("OWN ROUTE", size=16, color=MUT).move_to([-2.05, -1.05, 0])
        self.play_at(5.26, Create(routes), FadeIn(ol), run_time=0.8)

        ring = Circle(radius=1.55, color=GREEN, stroke_width=3).move_to(
            [-2.05, 0.05, 0])
        tl = chip("TEAM OBJECTIVE", color=GREEN, size=18).move_to([-2.05, -1.6, 0])
        self.play_at(6.98, Create(ring), FadeIn(tl), run_time=0.7)

        # competition panel
        rp = panel(5.7, 4.5, stroke=RED).move_to([2.55, 0, 0])
        rc = chip("COMPETITION", color=RED, size=23).move_to([2.55, 1.7, 0])
        og = label("OPPOSITE GOALS", size=18, color=RED).move_to([2.55, 1.15, 0])
        self.play_at(8.32, FadeIn(rp), FadeIn(rc), FadeIn(og), run_time=0.7)

        # chess board
        board = mini_grid(1.25, -0.95, 3, 3, cell=0.42, color=MUT)
        pw = Polygon([-0.16, 0, 0], [-0.05, 0.22, 0], [0.05, 0.22, 0],
                     [0.16, 0, 0], stroke_color=INK, stroke_width=2,
                     fill_color=INK, fill_opacity=0.7).move_to([1.88, -0.42, 0])
        pb = pw.copy().set_color(BLUE).move_to([2.3, -0.84, 0])
        wtag = chip("W", color=GREEN, size=18).move_to([3.35, -0.42, 0])
        ltag = chip("L", color=RED, size=18).move_to([3.35, -0.84, 0])
        cl = label("CHESS", size=17, color=MUT).move_to([1.95, -0.35 + 0.0, 0])
        cl.move_to([1.7, -1.62, 0])
        chess = VGroup(board, pw, pb, wtag, ltag, cl)
        self.play_at(11.62, FadeIn(chess), run_time=0.9)

        # same resources
        hexr = RegularPolygon(6, stroke_color=YELLOW, stroke_width=2.5,
                              fill_color=YELLOW, fill_opacity=0.25, start_angle=PI / 6)
        hexr.scale(0.30).move_to([3.0, -1.35, 0])
        b1 = Square(side_length=0.3, stroke_color=ORANGE, stroke_width=2.2,
                    fill_color=ORANGE, fill_opacity=0.2).move_to([1.7, -1.35, 0])
        b2 = b1.copy().set_color(PURPLE).move_to([4.3, -1.35, 0])
        a1 = Arrow(b1.get_right(), hexr.get_left(), buff=0.06, color=ORANGE,
                   stroke_width=2.4, tip_length=0.15)
        a2 = Arrow(b2.get_left(), hexr.get_right(), buff=0.06, color=PURPLE,
                   stroke_width=2.4, tip_length=0.15)
        sl = label("SAME RESOURCES", size=16, color=MUT).move_to([3.0, -1.95, 0])
        res = VGroup(hexr, b1, b2, a1, a2, sl)
        self.play_at(14.26, FadeIn(res), run_time=0.9)

        self.wait_until(17.95)
        self.play_now(*cleanup(lp, lc, regs, drs, rl, routes, ol, ring, tl,
                               rp, rc, og, chess, res), run_time=0.6)
        self.finish()
