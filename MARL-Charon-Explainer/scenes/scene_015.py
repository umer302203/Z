from common import *  # noqa
from manim import *

# Scene 15 - Traffic management (280.84-304.62)
D = 23.78

class Scene015(SyncedScene):
    DURATION = D

    def construct(self):
        h1 = Line([-5.8, 1.2, 0], [5.8, 1.2, 0], stroke_color="#2c3644",
                  stroke_width=10)
        h2 = Line([-5.8, -1.6, 0], [5.8, -1.6, 0], stroke_color="#2c3644",
                  stroke_width=10)
        v1 = Line([-2.4, 3.0, 0], [-2.4, -3.4, 0], stroke_color="#2c3644",
                  stroke_width=10)
        v2 = Line([2.4, 3.0, 0], [2.4, -3.4, 0], stroke_color="#2c3644",
                  stroke_width=10)
        roads = VGroup(h1, h2, v1, v2)
        sig1 = traffic_light("red", 1.0).move_to([-2.4, 1.2, 0]).shift(UR * 0.32)
        sig2 = traffic_light("red", 1.0).move_to([2.4, 1.2, 0]).shift(UL * 0.32)
        sig3 = traffic_light("red", 1.0).move_to([0.4, -1.6, 0]).shift(UP * 0.55)
        sigs = VGroup(sig1, sig2, sig3)
        self.play_at(0.00, FadeIn(roads), FadeIn(sigs), run_time=0.8)

        rings = VGroup(*[Circle(radius=0.42, color=BLUE, stroke_width=2.5)
                         .move_to(s) for s in sigs])
        ag = chip("SIGNALS = AGENTS", color=BLUE, size=20).move_to([-4.5, 2.7, 0])
        self.play_at(6.60, Create(rings), FadeIn(ag), run_time=0.6)

        cones = VGroup(
            Polygon([-2.1, 1.5, 0], [-0.9, 2.0, 0], [-0.9, 0.9, 0],
                    stroke_color=BLUE, stroke_width=1.8, fill_color=BLUE,
                    fill_opacity=0.14),
            Polygon([2.7, 1.5, 0], [3.9, 2.0, 0], [3.9, 0.9, 0],
                    stroke_color=BLUE, stroke_width=1.8, fill_color=BLUE,
                    fill_opacity=0.14),
            Polygon([0.7, -1.0, 0], [1.7, -0.4, 0], [0.5, -0.25, 0],
                    stroke_color=BLUE, stroke_width=1.8, fill_color=BLUE,
                    fill_opacity=0.14),
        )
        ol = label("OBSERVE NEARBY", size=17, color=MUT).move_to([-4.4, 1.9, 0])
        self.play_at(9.16, FadeIn(cones), FadeIn(ol), run_time=0.7)

        links = VGroup(Line(sig1.get_center(), sig2.get_center(),
                            stroke_color=GREEN, stroke_width=2.4),
                       Line(sig2.get_center(), sig3.get_center(),
                            stroke_color=GREEN, stroke_width=2.4),
                       Line(sig1.get_center(), sig3.get_center(),
                            stroke_color=GREEN, stroke_width=2.4))
        gl3 = chip("COORDINATE", color=GREEN, size=20).move_to([4.5, 2.7, 0])
        self.play_at(11.96, Create(links), FadeIn(gl3), run_time=0.8)
        greens = [sig[3] for sig in sigs]  # green lamp dots
        self.play_at(12.80, *[g.animate.set_color(GREEN) for g in greens],
                     run_time=0.5)

        jam = VGroup(*[dot([x, y, 0], r=0.10, color=RED)
                       for x in np.linspace(1.4, 3.4, 5)
                       for y in [-1.75, -1.45]])
        jl = chip("JAM", color=RED, size=20).move_to([4.5, -2.5, 0])
        self.play_at(15.64, FadeIn(jam), FadeIn(jl), run_time=0.8)

        flow = VGroup(*[Arrow([x, 1.2, 0], [x + 0.9, 1.2, 0], buff=0.05,
                              color=GREEN, stroke_width=2.6, tip_length=0.16)
                        for x in [-4.6, -3.2]])
        nf = chip("NETWORK FLOW", color=GREEN, size=20).move_to([-4.3, -2.5, 0])
        self.play_at(20.78, FadeOut(jam), FadeIn(flow), FadeIn(nf),
                     rings.animate.set_stroke(GREEN), run_time=0.8)

        self.wait_until(23.0)
        self.play_now(*cleanup(roads, sigs, rings, ag, cones, ol, links, gl3,
                               jl, flow, nf), run_time=0.6)
        self.finish()
