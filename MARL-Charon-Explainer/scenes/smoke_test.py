from common import *  # noqa: F401,F403 - patches tex pipeline
from manim import *

class SmokeTest(Scene):
    def construct(self):
        self.camera.background_color = "#0b0e14"
        title = Text("MARL", font="sans-serif", weight=BOLD, color="#58a6ff", font_size=48)
        box = RoundedRectangle(corner_radius=0.2, width=4, height=2, stroke_color="#58a6ff", stroke_width=2)
        box.set_fill("#161b22", 0.6)
        title.move_to(box.get_center())
        arrow = Arrow(LEFT*3, box.get_left()+RIGHT*0.15, buff=0.1, color="#3fb950")
        eq = MathTex(r"Q(s,a) \leftarrow Q(s,a) + \alpha\left[r + \gamma \max_{a'} Q(s',a') - Q(s,a)\right]", font_size=30, color=WHITE)
        eq.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(box), Write(title), run_time=1)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.play(FadeIn(eq, shift=UP*0.2), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(VGroup(box, title, arrow, eq)), run_time=0.6)
