from common import *  # noqa
from manim import *

# Scene 29 - Learning stability (547.86-589.88)
D = 42.02

class Scene029(SyncedScene):
    DURATION = D

    def construct(self):
        # wavy policy line
        wave = FunctionGraph(lambda x: 0.35 * np.sin(2.4 * x) + 0.1 * np.sin(6 * x),
                             x_range=[-4.5, 4.5], color=BLUE, stroke_width=3)
        wave.move_to([0, 1.5, 0])
        st = chip("LEARNING STABILITY", color=ORANGE, size=22).move_to([0, 2.7, 0])
        self.play_at(0.00, Create(wave), FadeIn(st), run_time=0.8)

        # two policy cards rising alternately
        cardA = panel(1.9, 1.1, stroke=BLUE).move_to([-2.4, -0.7, 0])
        cardAl = label("AGENT A", size=17, color=BLUE).move_to(cardA)
        cardB = panel(1.9, 1.1, stroke=TEAL).move_to([2.4, -0.7, 0])
        cardBl = label("AGENT B", size=17, color=TEAL).move_to(cardB)
        cards = VGroup(cardA, cardAl, cardB, cardBl)
        self.play_at(2.66, FadeIn(cards), run_time=0.5)
        self.play_at(3.20, cardA.animate.shift(UP * 0.25),
                     cardB.animate.shift(DOWN * 0.1), run_time=0.4)
        self.play_at(3.65, cardB.animate.shift(UP * 0.35), run_time=0.4)

        # yesterday works, today fails
        yt = chip("WORKS YESTERDAY", color=GREEN, size=17).move_to([-2.4, 0.5, 0])
        self.play_at(7.14, FadeIn(yt), run_time=0.5)
        ft = chip("FAILS TODAY", color=RED, size=17).move_to([-2.4, 0.62, 0])
        self.play_at(8.20, FadeOut(yt), FadeIn(ft),
                     cardA.animate.set_stroke(RED), run_time=0.5)

        # traffic drivers example
        road = Rectangle(width=8.6, height=1.0, stroke_color=GRIDC,
                         stroke_width=2, fill_color="#182130",
                         fill_opacity=1).move_to([0.4, -2.6, 0])
        dashes = VGroup(*[Line([-3.6 + 0.55 * i, -2.6, 0], [-3.32 + 0.55 * i, -2.6, 0],
                               stroke_color=MUT, stroke_width=2) for i in range(14)])
        roadg = VGroup(road, dashes)
        driver1 = car_icon(BLUE, 0.75).move_to([-3.0, -2.45, 0])
        drivers = VGroup(driver1)
        self.play_at(12.14, FadeIn(roadg), FadeIn(driver1), run_time=0.8)
        more = VGroup(*[car_icon(BLUE, 0.75).move_to([-2.0 + 0.75 * i, -2.45, 0])
                        for i in range(6)])
        slow = chip("SAME ROUTE = SLOW", color=RED, size=17).move_to(
            [0.4, -1.75, 0])
        self.play_at(14.82, LaggedStart(*[FadeIn(c, shift=LEFT * 0.2)
                                          for c in more], lag_ratio=0.12),
                     FadeIn(slow), run_time=0.9)
        pc = chip("PATTERN CHANGES", color=ORANGE, size=17).move_to(
            [0.4, -3.35, 0])
        self.play_at(18.50, *[c.animate.move_to([c.get_x() - 0.5, -2.75, 0])
                              for c in more[:3]],
                     FadeIn(pc), run_time=0.8)

        # environment tiles flipping
        tiles = VGroup()
        for i in range(12):
            for j in range(3):
                sq = Square(side_length=0.42, stroke_color="#1c242e",
                            stroke_width=1.2, fill_color="#141a22",
                            fill_opacity=0.8)
                sq.move_to([-5.4 + 0.46 * i, 0.9 - 0.46 * j, 0])
                tiles.add(sq)
        self.play_at(22.78, FadeOut(cards), FadeOut(ft), FadeIn(tiles),
                     run_time=0.9)
        for k, (t1, t2) in enumerate([(0, 1), (2, 1), (1, 2)]):
            flips = [tiles[i * 3 + j] for i in range(0, 12, 2)
                     for j in [t1 if i % 4 == 0 else t2]]
            self.play_at(23.80 + k * 0.45, *[
                t.animate.set_fill("#223046", 0.9) for t in flips
                if t.fill_opacity < 0.85], run_time=0.4)

        obs = chip("OBSERVE OTHERS", color=BLUE, size=19).move_to([-2.6, -1.6, 0])
        ada = chip("HANDLE UNCERTAINTY", color=TEAL, size=19).move_to([0.6, -1.6, 0])
        adr = chip("ADAPT", color=GREEN, size=19).move_to([3.4, -1.6, 0])
        self.play_at(30.06, FadeOut(tiles), FadeIn(obs), FadeIn(ada), FadeIn(adr),
                     run_time=0.8)

        opm = chip("OPPONENT MODELING", color=PURPLE, size=18).move_to(
            [-2.4, -2.7, 0])
        pbt = chip("POPULATION TRAINING", color=PURPLE, size=18).move_to(
            [1.2, -2.7, 0])
        res = label("RESEARCH DIRECTIONS", size=15, color=MUT).move_to(
            [-0.6, -3.3, 0])
        self.play_at(35.04, FadeIn(opm), FadeIn(pbt), FadeIn(res), run_time=0.8)

        self.wait_until(41.2)
        self.play_now(*cleanup(wave, st, roadg, drivers, more, slow, pc, obs,
                               ada, adr, opm, pbt, res), run_time=0.6)
        self.finish()
