from common import *  # noqa
from manim import *

# Scene 14 - Partial observability (239.62-280.84)
D = 41.22

class Scene014(SyncedScene):
    DURATION = D

    def construct(self):
        # two corridor panels with a wall between
        cl = panel(4.0, 3.1, stroke=BLUE).move_to([-2.35, 0, 0])
        cr = panel(4.0, 3.1, stroke=TEAL).move_to([2.35, 0, 0])
        wall = Rectangle(width=0.35, height=3.5, stroke_color=MUT,
                         stroke_width=2.5, fill_color="#242c38",
                         fill_opacity=0.9).move_to([0, 0, 0])
        ra = robot_icon(BLUE, 0.95).move_to([-3.4, -0.7, 0])
        rb = robot_icon(TEAL, 0.95).move_to([3.4, -0.7, 0])
        corr = VGroup(cl, cr, wall, ra, rb)
        self.play_at(0.00, FadeIn(corr), run_time=0.8)

        # view cones + fog
        cone_l = Polygon([-3.4, -0.7, 0], [-1.7, 0.35, 0], [-1.7, -1.55, 0],
                         stroke_color=BLUE, stroke_width=2,
                         fill_color=BLUE, fill_opacity=0.15)
        cone_r = Polygon([3.4, -0.7, 0], [1.7, 0.35, 0], [1.7, -1.55, 0],
                         stroke_color=TEAL, stroke_width=2,
                         fill_color=TEAL, fill_opacity=0.15)
        fog_l = VGroup(*[dot([x, y, 0], r=0.09, color="#3a4353", opacity=0.75)
                         for x, y in [(-3.0, 0.75), (-2.45, 1.0), (-3.3, 1.15),
                                      (-2.0, 0.6)]])
        fog_r = VGroup(*[dot([x, y, 0], r=0.09, color="#3a4353", opacity=0.75)
                         for x, y in [(3.0, 0.75), (2.45, 1.0), (3.3, 1.15),
                                      (2.0, 0.6)]])
        vlabel = label("ONLY OWN CORRIDOR", size=17, color=MUT).move_to([0, 1.92, 0])
        self.play_at(5.58, FadeIn(cone_l), FadeIn(cone_r), FadeIn(fog_l),
                     FadeIn(fog_r), FadeIn(vlabel), run_time=0.9)

        hl = chip("HIDDEN INFO", color=MUT, size=17).move_to([-2.65, 1.35, 0])
        hr = chip("HIDDEN INFO", color=MUT, size=17).move_to([2.65, 1.35, 0])
        self.play_at(13.32, FadeIn(hl), FadeIn(hr), run_time=0.6)

        mem = panel(1.3, 0.6, stroke=PURPLE)
        mem_l = label("MEMORY", size=15, color=PURPLE).move_to(mem)
        memg = VGroup(mem, mem_l).move_to([-1.35, 2.5, 0])
        chat = panel(1.3, 0.6, stroke=GREEN)
        chat_l = label("COMMS", size=15, color=GREEN).move_to(chat)
        chatg = VGroup(chat, chat_l).move_to([1.35, 2.5, 0])
        self.play_at(14.56, FadeOut(hl), FadeOut(hr), FadeIn(memg), FadeIn(chatg),
                     run_time=0.7)

        bub = bubble("LEFT CORRIDOR: DONE", color=GREEN, size=16, tail=None)
        bub.move_to([2.35, 0.6, 0])
        tick = polyline_check(GREEN, 0.55).next_to(bub, LEFT, buff=0.14)
        msg = Arrow(chatg.get_right(), bub.get_top() + LEFT * 0.3, buff=0.08,
                    color=GREEN, stroke_width=2.4, tip_length=0.16)
        self.play_at(19.22, FadeIn(bub), FadeIn(tick), GrowArrow(msg),
                     run_time=0.7)

        # right robot moves to new area
        newb = robot_icon(TEAL, 0.95).move_to([1.35, -0.7, 0])
        self.play_at(22.92, Transform(rb, newb), run_time=0.8)

        # observe and guess intentions
        obs = DashedLine([-1.35, -0.35, 0], [1.35, -0.35, 0], dash_length=0.1,
                         stroke_color=PURPLE, stroke_width=2.4)
        qm = label("?", size=24, color=PURPLE).move_to([0, 0.05, 0])
        gl = label("GUESS INTENT", size=16, color=PURPLE).move_to([0, -0.75, 0])
        self.play_at(29.10, FadeOut(bub), FadeOut(tick), FadeOut(msg),
                     Create(obs), FadeIn(qm), FadeIn(gl), run_time=0.7)

        # share only useful info
        funnel = VGroup(Polygon([-0.5, 0.35, 0], [0.5, 0.35, 0], [0.12, -0.1, 0],
                                [-0.12, -0.1, 0], stroke_color=YELLOW,
                                stroke_width=2.5, fill_color=YELLOW,
                                fill_opacity=0.2),
                        Rectangle(width=0.24, height=0.42, stroke_color=YELLOW,
                                  stroke_width=2.5, fill_color=YELLOW,
                                  fill_opacity=0.2).move_to([0, -0.32, 0]))
        funnel.move_to([0, 1.35, 0])
        fl = chip("USEFUL INFO ONLY", color=YELLOW, size=19).move_to([0, 2.35, 0])
        p1 = Line([-3.4, 0.55, 0], [-0.65, 1.28, 0], stroke_color=BLUE,
                  stroke_width=2)
        p2 = Line([3.4, 0.55, 0], [0.65, 1.28, 0], stroke_color=TEAL,
                  stroke_width=2)
        self.play_at(38.08, FadeIn(funnel), FadeIn(fl), Create(p1), Create(p2),
                     run_time=0.8)

        self.wait_until(40.45)
        self.play_now(*cleanup(corr, cone_l, cone_r, fog_l, fog_r, vlabel, memg,
                               chatg, obs, qm, gl, funnel, fl, p1, p2),
                      run_time=0.6)
        self.finish()
