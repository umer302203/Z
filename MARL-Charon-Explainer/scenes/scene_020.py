from common import *  # noqa
from manim import *

# Scene 20 - Scalability (392.90-405.40)
D = 12.50

class Scene020(SyncedScene):
    DURATION = D

    def construct(self):
        lim = chip("LIMIT 2: SCALABILITY", color=ORANGE, size=22)
        lim.move_to([-3.6, 2.6, 0])
        self.play_at(0.00, FadeIn(lim), run_time=0.7)

        # 3-node mesh
        p1 = agent_node("A", BLUE, r=0.26).move_to([-4.6, 0.9, 0])
        p2 = agent_node("B", TEAL, r=0.26).move_to([-3.4, 0.9, 0])
        p3 = agent_node("C", PURPLE, r=0.26).move_to([-4.0, -0.2, 0])
        mesh3 = VGroup(Line(p1.get_center(), p2.get_center(), stroke_color=MUT,
                            stroke_width=2),
                       Line(p1.get_center(), p3.get_center(), stroke_color=MUT,
                            stroke_width=2),
                       Line(p2.get_center(), p3.get_center(), stroke_color=MUT,
                            stroke_width=2))
        m3 = VGroup(mesh3, p1, p2, p3)
        m3l = label("3 AGENTS: 3 LINKS", size=17, color=MUT).move_to([-4.0, -1.15, 0])
        self.play_at(0.54, FadeIn(m3), FadeIn(m3l), run_time=0.7)

        # swarm of dots
        rng = np.random.default_rng(7)
        pts = []
        for i in range(26):
            x = rng.uniform(-1.2, 5.6)
            y = rng.uniform(-2.2, 2.2)
            if abs(x) < 0.5 and abs(y) < 0.5:
                x += 1.2
            pts.append([x, y, 0])
        swarm = VGroup(*[dot(p, r=0.09, color=BLUE if i % 2 else TEAL,
                             opacity=0.85) for i, p in enumerate(pts)])
        cnt = chip("100 AGENTS: 4950 LINKS", color=RED, size=21).move_to(
            [2.2, 2.6, 0])
        self.play_at(4.78, FadeOut(m3), FadeOut(m3l), FadeIn(swarm), FadeIn(cnt),
                     run_time=1.0)

        few = VGroup(*[Line(swarm[i].get_center(), swarm[j].get_center(),
                            stroke_color=RED, stroke_width=1.4,
                            stroke_opacity=0.6)
                       for i, j in [(0, 1), (1, 2), (2, 3), (0, 3), (4, 5),
                                    (5, 6), (6, 7), (4, 7), (8, 9), (9, 10)]])
        expl = chip("INTERACTIONS EXPLODE", color=RED, size=21).move_to(
            [2.2, -2.75, 0])
        self.play_at(7.10, FadeIn(few), FadeIn(expl), run_time=0.8)

        self.wait_until(11.7)
        self.play_now(*cleanup(lim, swarm, cnt, few, expl), run_time=0.6)
        self.finish()
