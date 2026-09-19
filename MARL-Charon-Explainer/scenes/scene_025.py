from common import *  # noqa
from manim import *

# Scene 25 - Learning from learners (466.10-487.62)
D = 21.52

class Scene025(SyncedScene):
    DURATION = D

    def construct(self):
        c1 = chip("INDIVIDUAL DECISIONS", color=BLUE, size=19).move_to([-2.4, 2.3, 0])
        c2 = chip("TEAM OUTCOME", color=TEAL, size=19).move_to([2.4, 2.3, 0])
        fwd = Arrow(c1.get_right(), c2.get_left(), buff=0.12, color=MUT,
                    stroke_width=2.8, tip_length=0.2)
        bck = Arrow(c2.get_left() + DOWN * 0.3, c1.get_right() + DOWN * 0.3,
                    buff=0.12, color=MUT, stroke_width=2.8, tip_length=0.2)
        self.play_at(0.00, FadeIn(c1), FadeIn(c2), GrowArrow(fwd), GrowArrow(bck),
                     run_time=0.8)

        # single-agent loop
        loop1 = Arc(radius=0.85, start_angle=-0.6, angle=TAU - 1.2,
                    stroke_color=BLUE, stroke_width=3).move_to([-3.4, -0.7, 0])
        loop1.add_tip(tip_length=0.2, tip_width=0.2)
        s1 = agent_node("S", BLUE, r=0.24).move_to([-3.4, -0.7, 0])
        e1 = label("ENV", size=16, color=MUT).move_to([-3.4, -1.85, 0])
        l1 = label("SINGLE-AGENT: LEARNS FROM ENVIRONMENT", size=16, color=MUT)
        l1.move_to([-3.4, 0.6, 0])
        sing = VGroup(loop1, s1, e1, l1)
        self.play_at(5.46, FadeIn(sing), run_time=0.8)

        # multi-agent: learns also from other learners
        loop2 = Arc(radius=0.85, start_angle=-0.6, angle=TAU - 1.2,
                    stroke_color=TEAL, stroke_width=3).move_to([2.6, -0.7, 0])
        loop2.add_tip(tip_length=0.2, tip_width=0.2)
        s2 = agent_node("S", TEAL, r=0.24).move_to([2.6, -0.7, 0])
        o2 = agent_node("O", PURPLE, r=0.24).move_to([4.3, -0.7, 0])
        cross = Arrow(s2.get_right(), o2.get_left(), buff=0.08, color=PURPLE,
                      stroke_width=2.6, tip_length=0.18)
        cross2 = Arrow(o2.get_left() + DOWN * 0.2, s2.get_right() + DOWN * 0.2,
                       buff=0.08, color=PURPLE, stroke_width=2.6, tip_length=0.18)
        l2 = label("MULTI-AGENT: ALSO FROM OTHER LEARNERS", size=16, color=MUT)
        l2.move_to([2.9, 0.6, 0])
        multi = VGroup(loop2, s2, o2, cross, cross2, l2)
        self.play_at(8.26, FadeIn(multi), run_time=0.8)

        # shared world icon pairs
        row_y = -2.6
        car1 = car_icon(BLUE, 0.8).move_to([-3.6, row_y, 0])
        car2 = car_icon(ORANGE, 0.8).move_to([-2.4, row_y, 0])
        roadbar = Line([-4.1, row_y - 0.35, 0], [-1.9, row_y - 0.35, 0],
                       stroke_color=GRIDC, stroke_width=4)
        rob1 = robot_icon(TEAL, 0.75).move_to([-0.7, row_y + 0.05, 0])
        rob2 = robot_icon(PURPLE, 0.75).move_to([0.5, row_y + 0.05, 0])
        floorbar = Line([-1.2, row_y - 0.35, 0], [1.0, row_y - 0.35, 0],
                        stroke_color=GRIDC, stroke_width=4)
        dr1 = drone_icon(BLUE, 0.75).move_to([2.4, row_y + 0.15, 0])
        dr2 = drone_icon(TEAL, 0.75).move_to([3.6, row_y + 0.15, 0])
        infolink = Line(dr1.get_right(), dr2.get_left(), stroke_color=GREEN,
                        stroke_width=2.2)
        shared = VGroup(car1, car2, roadbar, rob1, rob2, floorbar, dr1, dr2,
                        infolink)
        sl = label("SHARED ROADS, WAREHOUSES, INFORMATION", size=16, color=MUT)
        sl.move_to([0, row_y - 0.85, 0])
        self.play_at(12.74, FadeIn(shared), FadeIn(sl), run_time=1.0)

        self.wait_until(20.9)
        self.play_now(*cleanup(c1, c2, fwd, bck, sing, multi, shared, sl),
                      run_time=0.55)
        self.finish()
