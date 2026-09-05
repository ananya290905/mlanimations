import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

# define function for the 3d loss graph
def loss_surface(u, v):
    z = (
        0.6 * np.sin(u) * np.cos(v)
        + 0.4 * np.sin(2 * u + 1) * np.cos(v - 1)
        + 0.15 * (u ** 2 + v ** 2) * 0.05
    )
    return np.array([u, v, z])

def surface_z(x, y):
    # same function just returns z for a given (x, y)
    return (
        0.6 * np.sin(x) * np.cos(y)
        + 0.4 * np.sin(2 * x + 1) * np.cos(y - 1)
        + 0.15 * (x ** 2 + y ** 2) * 0.05
    )

# calcualte gradient at a specific point in time
def gradient(x, y, eps=1e-3):
    dzdx = (surface_z(x + eps, y) - surface_z(x - eps, y)) / (2 * eps)
    dzdy = (surface_z(x, y + eps) - surface_z(x, y - eps)) / (2 * eps)
    return np.array([dzdx, dzdy])

class GDExplainedScene(ThreeDScene, VoiceoverScene):

    def construct(self):
        self.set_speech_service(RecorderService(transcription_model=None))

        self.equation = MathTex(
            r"{{\theta_{\text{new}}}}",
            r"{{=}}",
            r"{{\theta_{\text{old}}}}",
            r"-",
            r"{{\alpha}}",
            r"{{\nabla J}}",
            r"(",
            r"{{\theta}}",
            r")",
        ).set_color(WHITE).scale(1.5)

        self.gradient_descent_3d()
        self.explain_equation()
        self.example()
        self.alpha_differences()
        self.ending()

    def gradient_descent_3d(self):

        self.set_camera_orientation(phi=55 * DEGREES, theta=90 * DEGREES, distance=8)

        # make the surface of the curve
        surface = Surface(
            loss_surface,
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(32, 32),
            fill_opacity=0.85,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        with self.voiceover(text='Imagine you had to find the lowest point of this graph.') as tracker:
            # create surface
            self.play(Create(surface), run_time=1.5)
            self.wait(max(0, tracker.duration - 1.5))

        # starting point of dot
        with self.voiceover(text='You might want to start at a random point') as tracker:
            x, y = 0.626, 0.476
            dot = Dot3D(
                point=[x, y, surface_z(x, y)],
                radius=0.12,
                color=RED,
            )
            self.play(FadeIn(dot, scale=0.5))

        with self.voiceover('and take a step towards the steepest way down till you have reached the bottom') as tracker:
            # trail behind dot
            trail = TracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=4)
            self.add(trail)

            # gradietn descent loop
            lr = 0.3
            num_steps = 20
            for _ in range(num_steps):
                grad = gradient(x, y)
                x -= lr * grad[0]
                y -= lr * grad[1]
                new_pos = [x, y, surface_z(x, y)]
                self.play(dot.animate.move_to(new_pos), run_time=0.15, rate_func=linear)

            self.wait(1)

    
            self.move_camera(
                phi=0,
                theta=-90 * DEGREES,
                distance=8,
                run_time=0.5
            )
        #    show the equation 
            self.play(
                FadeOut(surface),
                FadeOut(dot),
                FadeOut(trail),
                run_time=0.5
            )

    def explain_equation(self):


        with self.voiceover('This process is called gradient descent and can be described by this equation.') as tracker:

            self.add(self.equation)

        with self.voiceover(
            text="Here alpha represents the learning rate which determines how big a step we take"
        ) as tracker:

            self.play(
                self.equation.get_part_by_tex(r"\alpha").animate.set_color(RED),
                run_time=1
            )

            self.wait(max(0, tracker.duration - 1))

        with self.voiceover(
            text="and the gradient of J represents the direction of the steepest ascent which si why we subtract it to go down the slope"
        ) as tracker:

            self.play(
                self.equation.get_part_by_tex(r"\nabla J").animate.set_color(GREEN),
                run_time=1
            )

            self.wait(max(0, tracker.duration - 1))

        with self.voiceover(text="and theta represents the paramters we are trying to optimize") as tracker:
            
            self.play(
                self.equation.get_parts_by_tex(r"\theta").animate.set_color(BLUE),
                run_time=1
            )

            self.wait(max(0, tracker.duration - 1))
    
    def example(self):

        with self.voiceover(text="Let's try an example with a simpler 2D graph"):
            self.play(self.equation.animate.to_edge(UP).scale(0.8), run_time=1)
            highlight = self.equation.copy()
            highlight.next_to(self.equation, DOWN, buff=0.3).set_color(BLACK)
            self.play(FadeIn(highlight))
            axis = Axes(
                x_range=[-4, 4, 1],
                y_range=[-1, 5, 1],
                axis_config={"color": BLUE},
            ).scale(0.8).to_edge(DOWN)

            graph = axis.plot(lambda x: 0.5 * x ** 2, color=WHITE)

            self.play(Create(axis), Create(graph), run_time=1)

        with self.voiceover(text="Let's pick a random starting point, say we start up here") as tracker:
            left_dot = Dot(color=RED).move_to(axis.c2p(-3, 4.5)).scale(1.5)
            self.play(FadeIn(left_dot), run_time = 0.5)

            self.wait(max(0, tracker.duration - 0.5))

        with self.voiceover(text="Using derivatives") as tracker:
            left_tangent = Line(
                axis.c2p(-4, 7.5), axis.c2p(-2, 1.5), color=YELLOW
            )
            self.play(Create(left_tangent), run_time=0.7)

        
        with self.voiceover(text="we can see the gradient at this point is negative, meaning the slop is going donw") as tracker:
            negative_text = Tex("(-ve)", color=RED).move_to(axis.c2p(-2.2, 4.5)).scale(0.8*1.5)
            self.play(Write(negative_text))

        with self.voiceover(text="If we take out starting point"):

            theta_part = highlight[3]
            theta_old = MathTex(r"\theta_{\text{old}}", color=BLUE).move_to(left_dot.get_center()).scale(1.5 * 0.8)
            self.play(FadeIn(theta_old))

            self.play(theta_old.animate.move_to(theta_part.get_center()))
            theta_part.set_color(BLUE)
            self.remove(theta_old)

        with self.voiceover(
                text="and subtract alpha multiplied by the negative gradient"
            ):

            alpha_part = highlight.get_part_by_tex(r"\alpha")
            minus = highlight.get_part_by_tex(r"-")
            gradient_part = highlight.get_part_by_tex(r"\nabla J")

            alpha_part.set_color(GREEN)
            minus.set_color(RED)

            self.play(
                FadeIn(minus),
                FadeIn(alpha_part)
            )


            self.play(
                negative_text.animate.move_to(
                    gradient_part.get_center() + DOWN * 0.05 + RIGHT * 0.2
                )
            )  

            self.remove(left_tangent)

        with self.voiceover(text="cancels out so we are actually adding a positive number") as tracker:
            plus = MathTex("+").set_color(GREEN).move_to(minus.get_center())
            pos_text = Tex("(+ve)", color=GREEN).move_to(negative_text.get_center())

            self.play(
                ReplacementTransform(minus, plus),
                ReplacementTransform(negative_text, pos_text),
                run_time=0.8,
            )

                
        with self.voiceover(
            text="This moves us to the right, closer to the minimum"
        ):

            theta_new_part = highlight[0]

            eq = highlight.get_part_by_tex("=")

            # Make the θ_new and = visible
            theta_new_part.set_color(WHITE)
            eq.set_color(WHITE)

            # Move the point
            self.play(
                left_dot.animate.move_to(axis.c2p(-2, 2)),
                run_time=1
            )

            theta_new = theta_new_part.copy()
            self.add(theta_new)

            # Move the copy to the new point
            self.play(
                theta_new.animate.move_to(
                    left_dot.get_center()
                ),
                run_time=0.7
            )

            theta_new.set_color(BLUE)

        self.play(FadeOut(theta_new, plus, pos_text))
        highlight.set_color(BLACK)

        with self.voiceover('well what if we had started on the right side of the curve'):
         # well what if we had started on the right side of the curve
            self.play(left_dot.animate.move_to(axis.c2p(3, 4.5)))

        with self.voiceover('here the gradient will be positive as the slope is going up'):
        # here the gradient will be positive as the slope is going up
            right_tangent = Line(
                axis.c2p(4, 7.5), axis.c2p(2, 1.5), color=YELLOW
            )
            self.play(Create(right_tangent), run_time=0.7)

            positive_text = Tex("(+ve)", color=GREEN).move_to(axis.c2p(2.2, 4.5)).scale(0.8*1.5)
            self.play(Write(positive_text))

        with self.voiceover('if we take our current position and subtract alpha multiplied by a positive gradient, we move to the left'):
            # if we take our current position and subtract alpha multiplied y a positiove gradient , we move closer to the minimium 
            # by movign to the left 
            self.wait(6)
            self.remove(right_tangent, positive_text)
            self.play(left_dot.animate.move_to(axis.c2p(2, 2))) 

        with self.voiceover('this process is continued until changes become negligible'):
            # this process is continued until chnages become negligible
            for i in np.arange(2, -0.25, -0.25):
                self.play(
                    left_dot.animate.move_to(
                        axis.c2p(i, i ** 2 * 0.5)
                    ), run_time=0.2
                )

        self.clear()

    def alpha_differences(self):

        # keep in mind that the alpha aka the step size that you define affects this process
        with self.voiceover("Keep in mind that the alpha aka the step size that you define affects this process") as tracker:
            self.wait(tracker.duration)

        with self.voiceover("a step size too big?, you might overshoot the minimum"):
            # a step size too big? you might overshoot the minimum 
            laxis = Axes(
                x_range=[-4, 4, 1],
                y_range=[-1, 5, 1],
                axis_config={"color": BLUE},
            ).scale(0.8).to_edge(DOWN)

            graph = laxis.plot(lambda x: 0.5 * x ** 2, color=WHITE)

            self.play(Create(laxis), Create(graph), run_time=1)

            dot = Dot(color=RED).move_to(laxis.c2p(3, 4.5))
            self.play(Create(dot))

            prev = (3, 4.5)
            alpha = 1.8

            for i in range(7):
                # Gradient of f(x) = 0.5 * x^2 is x
                gradient = prev[0]

                # Gradient descent update
                new_x = prev[0] - alpha * gradient
                new_y = 0.5 * new_x ** 2

                new = (new_x, new_y)

                # Move dot
                self.play(
                    dot.animate.move_to(
                        laxis.c2p(new[0], new[1])
                    ), run_time=0.2
                )

                # Draw line between old and new point
                l = Line(
                    laxis.c2p(prev[0], prev[1]),
                    laxis.c2p(new[0], new[1]),
                    color=BLUE
                )

                self.play(Create(l), run_time=0.2)

                prev = new

        self.clear()
        with self.voiceover("a step size too small? it might take ages to find the minimum"):
            laxis = Axes(
                x_range=[-4, 4, 1],
                y_range=[-1, 5, 1],
                axis_config={"color": BLUE},
            ).scale(0.8).to_edge(DOWN)

            graph = laxis.plot(lambda x: 0.5 * x ** 2, color=WHITE)

            self.play(Create(laxis), Create(graph), run_time=1)

            dot = Dot(color=RED).move_to(laxis.c2p(3, 4.5))
            self.play(Create(dot))

            prev = (3, 4.5)
            alpha = 0.1

            for i in range(10):
                # Gradient of f(x) = 0.5 * x^2 is x
                gradient = prev[0]

                # Gradient descent update
                new_x = prev[0] - alpha * gradient
                new_y = 0.5 * new_x ** 2

                new = (new_x, new_y)

                # Move dot
                self.play(
                    dot.animate.move_to(
                        laxis.c2p(new[0], new[1])
                    ), run_time=0.2
                )

                # Draw line between old and new point
                l = Line(
                    laxis.c2p(prev[0], prev[1]),
                    laxis.c2p(new[0], new[1]),
                    color=BLUE
                )

                self.play(Create(l), run_time=0.2)

                prev = new
            self.clear()

            with self.voiceover('so it is essential that you pick an appropriate alpha for the task') as tracker:
                self.wait(tracker.duration)

        self.clear()

    def ending(self):

        with self.voiceover('well how is this important in the context of machine learning') as tracker:
            self.wait(tracker.duration)

        self.set_camera_orientation(phi=55 * DEGREES, theta=90 * DEGREES, distance=8)

        # make the surface of the curve
        surface = Surface(
            loss_surface,
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(32, 32),
            fill_opacity=0.85,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        with self.voiceover('if this graph now represents the loss function rpresenting how wrong our current predictions are'):
            # create surface
            self.play(Create(surface), run_time=1.5)
            self.wait(max(0, tracker.duration - 1.5))

        with self.voiceover('we can use gradient descent to find the weights required to get the lowest loss') as tracker:
            self.wait(tracker.duration)

        self.wait(1)
        self.clear()






