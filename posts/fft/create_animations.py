from manim import *
from contextlib import contextmanager
from typing import Generator


@contextmanager
def new_section(
    self,
    name: str = "unnamed",
    type: str = DefaultSectionType.NORMAL,
    skip_animations: bool = False,
) -> Generator[None, None, None]:
    print(f"Entering section: {name}")
    self.next_section(name, type, skip_animations)
    yield
    print(f"Exiting section: {name}")

    
Scene.new_section = new_section   


def evaluate_polynomial(x: float, coeffs: list) -> float:
    res = 0
    for i, coeff in enumerate(coeffs):
        res += coeff * x**i
    return res


# https://gist.github.com/uwezi/1bac36c5b418a2208e85a3a089f1516c
def clipPlot(csystem, plotfun, x_range=[-5,5,.01], **kwargs):
    grp = VGroup()
    dx = x_range[2]
    for xstart in np.arange(*x_range):
        snip = csystem.plot(
            plotfun,
            x_range = [xstart,xstart+dx,0.5*dx],
            **kwargs
        )
        if (snip.get_top()[1]>csystem.get_top()[1]) or (snip.get_bottom()[1]<csystem.get_bottom()[1]):
            #print(f"Start: {xstart} End: {xstart+dx}, SnipTop: {snip.get_top()[1]}, AxesTop: {csystem.get_top()[1]}, SnipBottom: {snip.get_bottom()[1]},  AxesBottom: {csystem.get_bottom()[1]}")
            snip.set_opacity(0)
        grp += snip
    return grp


class MultiplyPolynomials(Scene):
    def construct(self):
        p1 = MathTex("P(x)", "=", "x^2", "+", "4x", "+", "1").shift(1 * UP + 3 * LEFT)
        p2 = MathTex("F(x)", "=", "3x^2", "+", "x", "+", "4")

        r = MathTex("C(x)", "=", "3x^4", "+", "x^3", "+", "4x^2", "+", "12x^3", "+", "4x^2", "+", "16x", "+", "3x^2", "+", "x", "+", "4").shift(1 * DOWN)
        r_s = MathTex("C(x) = 3x^4 + 13x^3 + 11x^2 + 17x + 4").shift(1 * DOWN)


        p1_str = [x for x in range(2, len(p1), 2)]
        p2_str = [x for x in range(2, len(p2), 2)]
        out = [x for x in range(2, len(r), 2)]

        combs = []
        for x in p1_str:
            for y in p2_str:
                combs.append((x, y))

        p2.next_to(p1, RIGHT, buff=2)

        self.play(Create(p1), Create(p2))

        self.wait(1)

        self.play(
            *[
                TransformFromCopy(
                    VGroup(p1[t1], p2[t2]),
                    r[o],
                    run_time = 2,
                )
                for i, (t1, t2, o) in
                enumerate(
                    zip(
                        [x[0] for x in combs],
                        [x[1] for x in combs],
                        out
                    )
                )
            ]
            + [Create(r[0]), Create(r[1]), Create(r.get_parts_by_tex("+"))]
        )

        self.wait(2)

        self.play(
            Transform(r, r_s)
        )

        self.wait()


class MultiplyPolynomialsPointwise(Scene):
    def construct(self):

        p1 = MathTex("P(x)", "=", "x^2", "+", "4x", "+", "1", color=ORANGE).shift(3 * UP + 3 * LEFT)
        p2 = MathTex("F(x)", "=", "3x^2", "+", "x", "+", "4", color=BLUE).next_to(p1, RIGHT, buff=1)
        r_s = MathTex("C(x) = 3x^4 + 13x^3 + 11x^2 + 17x + 4", color=GREEN).next_to(p1, DOWN, buff=.5).shift(3 * RIGHT)

        textvg = VGroup(p1, p2, r_s).scale(.75)

        self.play(Write(textvg))

        self.wait(2)

        eval_points = [-3.732, -2, -0.268, 0, .5]

        p1_points = [(x, evaluate_polynomial(x, [1, 4, 1])) for x in eval_points]
        p2_points = [(x, evaluate_polynomial(x, [4, 1, 3])) for x in eval_points]
        out_points = [(x, evaluate_polynomial(x, [4, 17, 11, 13, 3])) for x in eval_points]

        p1_points_text = ", ".join([f"({x}, {y:.2f})" for x, y in p1_points])
        p1_points_text = MathTex(p1_points_text, color=ORANGE).scale(.75)

        p2_points_text = ", ".join([f"({x}, {y:.2f})" for x, y in p2_points])
        p2_points_text = MathTex(p2_points_text, color=BLUE).scale(.75).next_to(p1_points_text, DOWN, aligned_edge=LEFT)

        mult = MathTex(r"\times").scale(0.5).next_to(p2_points_text, LEFT)
        line = Underline(p2_points_text)

        out_points_text = ", ".join([f"({x}, {y:.2f})" for x, y in out_points])
        out_points_text = MathTex(out_points_text, color=GREEN).scale(.75).next_to(line, DOWN, aligned_edge=LEFT)

        self.play(
            FadeIn(p1_points_text),
            FadeIn(p2_points_text),
            FadeIn(mult),
            Create(line),
            FadeIn(out_points_text)
        )

        self.wait(7)

        self.play(
            FadeOut(p1_points_text),
            FadeOut(p2_points_text),
            FadeOut(mult),
            FadeOut(line),
            FadeOut(out_points_text)
        )

        self.wait(1)

        p1_points = [x for x in p1_points if x[1] < 8 and x[1] > -8]
        p2_points = [x for x in p2_points if x[1] < 8 and x[1] > -8]
        out_points = [x for x in out_points if x[1] < 8 and x[1] > -8]

        ax = Axes(
            x_range=[-5, 5, 1], y_range=[-8, 8, 1], axis_config={"include_tip": False},
        ).add_coordinates().scale(0.75)
        labels = ax.get_axis_labels(x_label="x", y_label="y")

        p1_func = lambda x: 1 + 4 * x + x ** 2
        p2_func = lambda x: 4 + x + 3 * x ** 2
        out_func = lambda x: 4 + (17 * x) + (11 * x ** 2) + (13 * x ** 3) + (3 * x ** 4)
        
        graph = clipPlot(ax, plotfun=p1_func, x_range=[-5, 5, 000.1], color=ORANGE)
        graph2 = clipPlot(ax, plotfun=p2_func, x_range=[-5, 5, 000.1], color=BLUE)
        graph3_r = clipPlot(ax, plotfun=out_func, x_range=[-2, 5, 000.1], color=GREEN).shift(1 * DOWN)
        graph3_l = clipPlot(ax, plotfun=out_func, x_range=[-3.8, -3.6, 0.001], color=GREEN).shift(1 * DOWN)

        p1_dots = [Dot(ax.c2p(x, y), color=ORANGE) for x, y in p1_points]
        p2_dots = [Dot(ax.c2p(x, y), color=BLUE) for x, y in p2_points]
        out_dots = [Dot(ax.c2p(x, y), color=GREEN).shift(1 * DOWN) for x, y in out_points]

        graph_group = VGroup(ax, graph, graph2, labels, *p1_dots, *p2_dots).shift(1 * DOWN)

        self.play(Write(graph_group))

        self.wait(2)   

        print(ax.get_top(), ax.get_bottom(), ax.get_left(), ax.get_right())

        self.play (
            FadeIn(graph3_l),
            FadeIn(graph3_r),
            FadeIn(VGroup(*out_dots)),
        )

        self.wait(7)     


class LagrangeInterpolation(Scene):
    def construct(self):
        with self.new_section("Intro"):
            points = MathTex("(0, 0), (1, 1), (-1, 1)").shift(4 * LEFT)
            equals = MathTex("=").next_to(points, RIGHT)

            ax = Axes(
                x_range=[-2, 2, 1], y_range=[-2, 2, 1], axis_config={"include_tip": False},
            ).add_coordinates().scale(0.5).next_to(equals, RIGHT)  

            graph = ax.plot(lambda x: x**2, x_range=[-1.4,1.4,0.01], color=BLUE)

            question = MathTex("?").next_to(ax, RIGHT)

            p1 = Dot(ax.c2p(0, 0), color=BLUE)
            p2 = Dot(ax.c2p(1, 1), color=BLUE)
            p3 = Dot(ax.c2p(-1, 1), color=BLUE)

            self.play(
                FadeIn(points),
                FadeIn(equals),
                FadeIn(ax),
            )

            self.play(
                Write(graph),
                Write(p1),
                Write(p2),
                Write(p3),
                FadeIn(question),
            )

            self.wait(3)

            self.play(
                FadeOut(points),
                FadeOut(equals),
                FadeOut(graph),
                FadeOut(p1),
                FadeOut(p2),
                FadeOut(p3),
                FadeOut(question),
                FadeOut(ax),
            )
        with self.new_section("Definition"):
            title = Text("Lagrange Interpolation", color=RED).shift(3 * UP)
            px = MathTex("\Sigma_{i=0}^n P_i(x)").shift(1.5 * UP).scale(1.2)
            where = Text("where", color=YELLOW).shift(1 * UP).scale(0.5).shift(.5 * DOWN)
            pi = MathTex(r"P_i(x) = y_i * \underset{j\neq i}{\prod_{j = 1}} \frac{x-x_j}{x_i - x_j").shift(1 * DOWN)

            res = MathTex(
                r"""
                    P(x) = 
                    \frac{(x - x_2)}{(x_1 - x_2)} *
                    \frac{(x - x_3)}{(x_1 - x_3)} * y_1 +
                    \frac{(x - x_1)}{(x_2 - x_1)} *
                    \frac{(x - x_3)}{(x_2 - x_3)} * y_2 +
                    \frac{(x - x_1)}{(x_3 - x_1)} *
                    \frac{(x - x_2)}{(x_3 - x_2)} * y_3
                """
            ).scale(.6)

            res_sub = MathTex(
                r"""
                    P(x) =
                    \frac{(x - 1)}{(0 - 1)} *
                    \frac{(x + 1)}{(0 + 1)} * 0 +
                    \frac{(x - 0)}{(1 - 0)} *
                    \frac{(x + 1)}{(1 + 1)} * 1 +
                    \frac{(x - 0)}{(-1 - 0)} *
                    \frac{(x - 1)}{(-1 - 1)} * 1
                """
            ).scale(.6)

            res_simplified = MathTex("P(x) = x^2")

            self.play(
                Write(title),
                Write(px),
                Write(where),
                Write(pi),
            )

            self.wait(5)

            self.play(
                FadeOut(where),
                FadeOut(pi),
            )

            self.play(
                px.animate.shift(1.5 * DOWN)
            )

            self.wait(1)

            self.play(
                Transform(px, res)
            )

            self.wait(3)

            self.play(
                Transform(px, res_sub)
            )

            self.wait(3)

            self.play(
                Transform(px, res_simplified)
            )

            self.wait(5)


class EvenAndOddPoints(Scene):
    def construct(self):
        even_polynomial = MathTex("P(x) = x^2").shift(3 * UP)
        odd_polynomial = MathTex("P(x) = x^3").shift(3 * UP)

        ax = Axes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1], axis_config={"include_tip": False},
        ).add_coordinates().scale(0.75).shift(1 * DOWN)

        even_graph = ax.plot(lambda x: x**2, x_range=[-1.4,1.4,0.01], color=BLUE)
        odd_graph = ax.plot(lambda x: x**3, x_range=[-1.4,1.4,0.01], color=GREEN)

        even_p1 = Dot(ax.c2p(1, 1), color=BLUE)
        even_p2 = Dot(ax.c2p(-1, 1), color=BLUE)

        even_p1_label = MathTex("(1, 1)").next_to(even_p1, UP).shift(1 * LEFT)
        even_p2_label = MathTex("(-1, 1)").next_to(even_p2, UP).shift(1 * RIGHT)

        odd_p1 = Dot(ax.c2p(1, 1), color=GREEN)
        odd_p2 = Dot(ax.c2p(-1, -1), color=GREEN)

        odd_p1_label = MathTex("(1, 1)").next_to(odd_p1, UP).shift(1 * LEFT)
        odd_p2_label = MathTex("(-1, -1)").next_to(odd_p2, UP).shift(2 * LEFT + .5 * DOWN)

        self.play(
            Write(even_polynomial),
            Write(ax),
            Write(even_graph),
            FadeIn(even_p1_label),
            Write(even_p1),
        )

        self.wait(2)

        self.play(
            FadeIn(even_p2_label),
            TransformFromCopy(even_p1, even_p2)
        )

        self.wait(3)

        self.play(
            FadeOut(even_p1_label),
            FadeOut(even_p2_label),
            FadeOut(even_p1),
            FadeOut(even_p2),
            FadeOut(even_graph),
            FadeOut(even_polynomial),
            
        )

        self.play(
            Write(odd_polynomial),
            Write(odd_graph),
            FadeIn(odd_p1),
            FadeIn(odd_p1_label),

        )

        self.wait(2)

        self.play(
            FadeIn(odd_p2_label),
            TransformFromCopy(odd_p1, odd_p2)
        )

        self.wait(3)


class RootsOfUnity(Scene):
    def construct(self):

        title = Text("Nth Roots of Unity", color=WHITE).shift(3.5 * UP + 4 * LEFT)
        title2 = Text("4th Roots of Unity", color=WHITE).shift(3.5 * UP + 4 * LEFT)
        title3 = Text("8th Roots of Unity", color=WHITE).shift(3.5 * UP + 4 * LEFT)

        numberplane = NumberPlane(background_line_style={"stroke_opacity": 0.5})

        circle = Circle(radius=3, color=YELLOW)

        one_point = Dot(circle.point_from_proportion(0), color=RED)
        neg_one_point = Dot(circle.point_from_proportion(0.5), color=RED)
        i_point = Dot(circle.point_from_proportion(0.25), color=RED)
        neg_i_point = Dot(circle.point_from_proportion(0.75), color=RED)

        one = MathTex("1").shift(3.5 * RIGHT + .5 * DOWN)
        neg_one = MathTex("-1").shift(2.5 * LEFT + .5 * DOWN)
        i = MathTex("i").shift(2.5 * UP + .5 * RIGHT)
        neg_i = MathTex("-i").shift(3.25 * DOWN + .5 * RIGHT)

        arrow = Arrow(
            start=ORIGIN,
            end=one_point.get_center(),
            buff=0,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        arrow2 = Arrow(
            start=ORIGIN,
            end=neg_one_point.get_center(),
            buff=0,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        arrow3 = Arrow(
            start=ORIGIN,
            end=i_point.get_center(),
            buff=0,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        arrow4 = Arrow(
            start=ORIGIN,
            end=neg_i_point.get_center(),
            buff=0,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )
        
        self.add(numberplane)

        self.play(
            Write(title),
            Write(circle),
            Write(one),
            Write(neg_one),
            Write(i),
            Write(neg_i),
            FadeIn(one_point),
            FadeIn(neg_one_point),
            FadeIn(i_point),
            FadeIn(neg_i_point),
            
        )

        self.wait(1)

        self.play(
            Transform(title, title2),
            Write(arrow),
            Write(arrow2),
            Write(arrow3),
            Write(arrow4),
        )

        arrow5 = Arrow(
            start=ORIGIN,
            end=circle.point_from_proportion(1/8),
            buff=0,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        arrow6 = Arrow(
            start=ORIGIN,
            end=circle.point_from_proportion(3/8),
            buff=0,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        arrow7 = Arrow(
            start=ORIGIN,
            end=circle.point_from_proportion(5/8),
            buff=0,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        arrow8 = Arrow(
            start=ORIGIN,
            end=circle.point_from_proportion(7/8),
            buff=0,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )

        point1 = Dot(circle.point_from_proportion(1/8), color=RED)
        point2 = Dot(circle.point_from_proportion(3/8), color=RED)
        point3 = Dot(circle.point_from_proportion(5/8), color=RED)
        point4 = Dot(circle.point_from_proportion(7/8), color=RED)

        self.wait(3)

        self.play(
            Transform(title, title3),
            Write(arrow5),
            Write(arrow6),
            Write(arrow7),
            Write(arrow8),
            FadeIn(point1),
            FadeIn(point2),
            FadeIn(point3),
            FadeIn(point4),
        )

        self.wait(3)