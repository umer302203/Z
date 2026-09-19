from manim import *

CYAN = "#58C4DD"  # classic manim cyan (removed constant in 0.21)


class SmokeTest(Scene):
    def construct(self):
        self.add(Text("MANIM OK", font_size=48).set_color(CYAN))
        box = Square().set_color(CYAN)
        self.play(Create(box), run_time=0.5)
        self.play(box.animate.scale(1.5), run_time=0.5)
        self.wait(0.3)
