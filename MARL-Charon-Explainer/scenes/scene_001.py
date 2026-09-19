from common import *  # noqa
from manim import *

# Scene 01 - Football analogy (0.00-19.50)
D = 19.50

class Scene001(SyncedScene):
    DURATION = D

    def construct(self):
        # pitch
        pitch = RoundedRectangle(corner_radius=0.18, width=7.4, height=4.2,
                                 stroke_color="#2ea043", stroke_width=3)
        pitch.set_fill("#0e1a12", 0.55)
        mid = Line(UP * 2.1, DOWN * 2.1, stroke_color="#2ea043", stroke_width=2)
        circ = Circle(radius=0.55, stroke_color="#2ea043", stroke_width=2)
        gl = Rectangle(width=0.5, height=1.5, stroke_color="#2ea043", stroke_width=2).move_to([-3.45, 0, 0])
        gr = gl.copy().move_to([3.45, 0, 0])
        pitch_g = VGroup(pitch, mid, circ, gl, gr)
        pitch_g.shift(LEFT * 0.1)
        self.play_at(0.00, FadeIn(pitch_g, scale=0.94), run_time=0.45)
        c1 = chip("ONE GROUND", color=GREEN, size=22).move_to([-2.6, 2.62, 0])
        self.play_at(0.50, FadeIn(c1, shift=UP * 0.15), run_time=0.4)
        c2 = chip("RULES SAME", color=GREEN, size=22).move_to([0.3, 2.62, 0])
        self.play_at(1.82, FadeIn(c2, shift=UP * 0.15), run_time=0.5)

        # players 10 vs 10
        B, O = BLUE, ORANGE
        blues = [(-3.2, 0), (-2.4, -1.3), (-2.4, 0), (-2.4, 1.3),
                 (-1.3, -0.8), (-1.3, 0.8), (-1.3, 0.0),
                 (-0.5, -0.9), (-0.5, 0.0), (-0.5, 0.9)]
        oranges = [(-x, -y) for (x, y) in blues]
        bdots = VGroup(*[dot([x - 0.1, y, 0], r=0.10, color=B) for x, y in blues])
        odots = VGroup(*[dot([x + 0.1, y, 0], r=0.10, color=O) for x, y in oranges])
        bdots.shift(LEFT * 0.1)
        odots.shift(LEFT * 0.1)
        self.play_at(4.18, LaggedStart(*[GrowFromCenter(d) for d in bdots] +
                                       [GrowFromCenter(d) for d in odots],
                                       lag_ratio=0.02), run_time=1.25)
        cnt = chip("20 PLAYERS", color=INK, size=22).move_to([5.35, 0.9, 0])
        self.play_at(5.50, FadeIn(cnt, shift=LEFT * 0.2), run_time=0.45)

        # focus player + decision
        fpos = np.array([-1.3 - 0.1, 0.8, 0])
        ring = Circle(radius=0.20, color=YELLOW, stroke_width=3).move_to(fpos)
        dec = chip("DECISION", color=YELLOW, size=19).move_to([-1.4, 1.62, 0])
        self.play_at(6.20, Create(ring), FadeIn(dec, shift=UP * 0.1), run_time=0.6)

        # sight lines: teammates & opponents
        mates = [np.array([-2.4 - 0.1, 1.3, 0]), np.array([-1.3 - 0.1, 0.0, 0])]
        foes = [np.array([1.3 + 0.1, -0.8, 0]), np.array([0.5 + 0.1, 0.0, 0])]
        ml = VGroup(*[DashedLine(fpos, m, dash_length=0.09, stroke_color=BLUE,
                                 stroke_width=2.2) for m in mates])
        ol = VGroup(*[DashedLine(fpos, f, dash_length=0.09, stroke_color=ORANGE,
                                 stroke_width=2.2) for f in foes])
        lm = label("TEAMMATES", size=17, color=BLUE).move_to([-2.75, 1.95, 0])
        lo = label("OPPONENTS", size=17, color=ORANGE).move_to([2.55, 1.95, 0])
        self.play_at(8.06, Create(ml), Create(ol), FadeIn(lm), FadeIn(lo),
                     run_time=1.1)

        # pass
        tgt = np.array([-0.5 - 0.1, 0.0, 0])
        pass_arr = Arrow(fpos, tgt, buff=0.14, color=BLUE, stroke_width=3,
                         tip_length=0.2)
        ball = dot(fpos + RIGHT * 0.02, r=0.055, color="#ffffff")
        self.play_at(11.26, Create(pass_arr), FadeIn(ball), run_time=0.5)
        self.play_at(11.76, MoveAlongPath(ball,
                     Line(fpos, tgt).scale(0.94)), run_time=0.7)

        # cover arcs behind focus
        cov = VGroup(Arc(radius=0.38, start_angle=PI * 0.62, angle=PI * 0.76,
                         stroke_color=TEAL, stroke_width=3),
                     Arc(radius=0.55, start_angle=PI * 0.70, angle=PI * 0.60,
                         stroke_color=TEAL, stroke_width=2))
        cov.shift(fpos)
        self.play_at(14.14, Create(cov), run_time=0.8)
        atk = Arrow(np.array([-0.6, 0.95, 0]), np.array([1.85, 1.4, 0]),
                    buff=0.12, color=BLUE, stroke_width=3, tip_length=0.2)
        atk.shift(LEFT * 0.1)
        self.play_at(15.60, GrowArrow(atk), run_time=0.7)

        # team result
        res = chip("TEAM RESULT +1", color=GREEN, size=22).move_to([5.35, 0.9, 0])
        up = Arrow([5.05, 0.35, 0], [5.05, 0.62, 0], buff=0.02, color=GREEN,
                   stroke_width=3, tip_length=0.16)
        self.play_at(17.04, FadeOut(cnt, shift=RIGHT * 0.2),
                     FadeIn(res, shift=LEFT * 0.2), GrowArrow(up), run_time=0.6)

        self.wait_until(18.95)
        self.play_now(*cleanup(pitch_g, bdots, odots, c1, c2, ring, dec, ml, ol,
                           lm, lo, cov, atk, res, up, ball, pass_arr),
                  run_time=0.5)
        self.finish()
