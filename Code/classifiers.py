import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class Bayes(VoiceoverScene):

    def construct(self):
        self.set_speech_service(RecorderService(transcription_model=None))
        self.nl = None
        self.oranges = None 
        self.apples = None 
        self.x_label = None
        self.intro()
        self.probability()
        self.examples()

    def intro(self):

        with self.voiceover("How can you tell the difference between apples and oranges?"):
            apple = ImageMobject('apple.png').move_to(LEFT * 3)
            orange = ImageMobject('orange.png').move_to(RIGHT * 3 + DOWN * 0.2).scale(0.9)

            self.play(FadeIn(apple, shift= UP))
            self.play(FadeIn(orange, shift= UP))

        
        with self.voiceover("Well I can take 20 apples"):
            n = 20
            # create 20 smaller apples
            self.apples = Group(*[
                ImageMobject("apple.png").scale(0.1)
                for _ in range(n)
            ])

            self.apples.arrange_in_grid(4, 5, 0.2).move_to(UP + LEFT * 3)
            self.play(FadeOut(apple), FadeIn(self.apples))

        with self.voiceover("and 20 oranges"):
            self.oranges = Group(*[
                ImageMobject("orange.png").scale(0.1)
                for _ in range(n)
            ])

            self.oranges.arrange_in_grid(4, 5, 0.2).move_to(UP + RIGHT * 3)
            self.play(FadeOut(orange), FadeIn(self.oranges))

        with self.voiceover("rate their sourness which we denote by x and plot it on the x axis like this like this"):
            np.random.seed(2)
            x_o = np.random.normal(0.75, 0.05, n)
            x_a = np.random.normal(0.55, 0.05, n)
            l, r = min(min(x_o), min(x_a)), max(max(x_o), max(x_a))
            self.nl = Axes([l - 0.1, r + 0.1], x_length=8).move_to(DOWN * 2).scale(1.5)
            self.x_label = self.nl.get_axis_labels(x_label="Sourness").scale(0.9)
            self.play(Create(self.nl))
            self.play(Write(self.x_label))
            
            # plot orange and apples
            for i in range(n):
                o = self.oranges[i] 
                a = self.apples[i] 
                self.play(o.animate.scale(0.7).move_to(self.nl.c2p(x_o[i])), run_time=0.01)
                self.play(a.animate.scale(0.7).move_to(self.nl.c2p(x_a[i])), run_time = 0.01)

        with self.voiceover("i can then draw a line to separate those two groups, where objects on the left of this line are assigned the apple class and object on the right are assigned the orange class but how do i actually decide where to draw this line?"):
            bound = Line(self.nl.c2p(0.67, 4), self.nl.c2p(0.67, -3))
            self.play(Create(bound))

        self.remove(bound)

    def probability(self):

        with self.voiceover("well for each object in this space, we should find p(y|x)," \
        " this notation means that we should find the probability that a fruit with a sourness x belongs to class y"):
            left = MathTex(r"p", r"(", r"y ", r"\mid", r"x", r")").move_to(UP * 2 + LEFT * 3).scale(1.5)
            self.play(Write(left))

        with self.voiceover("with a sourness x"):
            left.get_part_by_tex(r'x').set_color('RED')

        with self.voiceover("belongs to class y"):
            left.get_part_by_tex(r'y').set_color('GREEN')

        with self.voiceover("take for example this point on the left, it has a low sourness score so the probability that a fruit with this value of sourness is assigned to the apple class is high"):
            a = self.apples[12]
            arrow_1 = Arrow(a.get_center() + 2 * UP, a.get_center() + 0.2 * UP)
            self.play(Create(arrow_1))
        self.remove(arrow_1)

        with self.voiceover("similarily, given a fruit has a high sourness level, like this one of the right side, the probability that it is part fo the orange class is high"):

            o = self.oranges[3]
            self.play(arrow_1.animate.put_start_and_end_on(o.get_center() + 2 * UP, o.get_center() + 0.2 * UP))


        with self.voiceover("it is important to note that the probability that a given x to any class should add up to 1") as tracker:
            self.wait(tracker.duration)
            


        with self.voiceover("this value can be calculated using bayes theorem"):
            self.remove(self.nl, self.oranges, self.apples, self.x_label, arrow_1)
            self.play(left.animate.move_to(ORIGIN + LEFT * 2))
            rest = MathTex(
                r"= \frac{p(x \mid y) p(y)}{p(x)}"
            ).scale(1.5).next_to(left, RIGHT)


            self.play(Write(rest))

        with self.voiceover("here p(y|x) is called the class posterior probability, p(x|y) is called the class conditional distribution" \
                        ", p(y) is the class prior and p(x) is the data distribtion"):
            
            posterior_label = Text("Class Posterior \n Probability").scale(0.5).move_to(left.get_bottom() + DOWN * 0.5)
            conditional_label = Text("Class \nConditional \nDistribution").scale(0.5).move_to(posterior_label.get_center() + RIGHT * 3.5 + UP * 2.5)
            prior_label = Text("Class Prior").scale(0.5).move_to(conditional_label.get_center() + RIGHT * 2 + DOWN * 0.3)
            distribution_label = Text("Data Distribution").scale(0.5).move_to(posterior_label.get_center() + RIGHT * 4 + DOWN * 0.5)

            self.play(Write(posterior_label), Write(conditional_label), Write(prior_label), Write(distribution_label))

        with self.voiceover("so lets see how we can find the values of each of these"):
            self.remove(posterior_label, conditional_label, prior_label, distribution_label)
            self.play(left.animate.scale(0.5).move_to(LEFT * 6 + UP * 3))
            self.play(rest.animate.scale(0.5).next_to(left, RIGHT))

    def examples(self):


        with self.voiceover("the class conditional probability shows the distribution of the data for each class") as tracker:
            self.wait(tracker.duration)

        with self.voiceover("for simiplicity lets model each class's sourness level as a gaussian distribution"):

            self.play(Create(self.nl), FadeIn(self.apples), FadeIn(self.oranges))
            mu_apple = 0.55
            mu_orange = 0.75
            sigma = 0.1

            # define these once, above, so you can reuse them
            def gaussian(mu, sigma):
                return lambda x: (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

            apple_pdf = gaussian(mu_apple, sigma)
            orange_pdf = gaussian(mu_orange, sigma)

            apple_dist = self.nl.plot(apple_pdf, x_range=[0.2, 1.1], color=RED)
            orange_dist = self.nl.plot(orange_pdf, x_range=[0.2, 1.1], color=ORANGE)

            self.play(
                Create(apple_dist),
                Create(orange_dist)
            )

        with self.voiceover("if you remember y represented our classes which were" \
        " apples and oranges so these curves shows p(x|apple) and p(x|orange)"):
            
            p_apple = MathTex("p(x | apple)").move_to(UP * 2.7 + LEFT * 1.8).scale(0.7)
            p_orange = MathTex("p(x | orange)").move_to(UP * 2.7 + RIGHT * 2.3).scale(0.7)
            self.play(Write(p_apple), Write(p_orange))

        with self.voiceover("next we find the class priors p(y), this can be usually calculated with the data we already have"):
            p_y = MathTex(r"p(y)").move_to(UP * 3 + RIGHT * 4.5).scale(0.7)
            self.play(Write(p_y))

        with self.voiceover("from before we know that we have 20 apples and 20 oranges, so the probability of an apple can be" \
        "modeled as 20 / 40 or 0.5"):
            p_y_a = MathTex(r"= p(apple) = \frac{20}{40}").move_to(UP * 2.5 + RIGHT * 5.2).scale(0.7)
            self.play(Write(p_y_a))

        with self.voiceover("similarly the probability of an orange would be 0.5 as well"):
            p_y_o = MathTex(r"= p(orange) = \frac{20}{40}").move_to(UP * 1.5 + RIGHT * 5.3).scale(0.7)
            self.play(Write(p_y_o))

        with self.voiceover("according to the equation we now mutiply the class priors wiht our class conditionals which would look like this"):
            self.remove(p_apple, p_orange)
            self.wait(5)

            apple_post = self.nl.plot(lambda x: 0.5 * apple_pdf(x), x_range=[0.2, 1.1], color=RED)
            orange_post = self.nl.plot(lambda x: 0.5 * orange_pdf(x), x_range=[0.2, 1.1], color=ORANGE)

            self.play(
                Transform(apple_dist, apple_post),
                Transform(orange_dist, orange_post)
            )

        self.remove(p_y_a, p_y_o, p_y)

        with self.voiceover("and finally the p(x), since this doesnt depend on the classes, it doesnt change" \
        "which posterior probability is higher but we can calcualte it by summing the class condition distribution multiplied by " \
        "the class prior for every class"):
            p_x = MathTex(r"p(x) = \sum_{c \in C} p(x \mid c)p(c)").move_to(UP * 3 + RIGHT * 4.5).scale(0.7)

            self.play(Write(p_x))

        with self.voiceover("so we end up with this graph, we can see which class has" \
        " the highest class posterior probability and we assign the object to the highest class") as tracker:
            self.remove(p_x)
            self.wait(tracker.duration)

        with self.voiceover("we draw the the decision boundary where the graphs intersect since anything to" \
        "the left of the line, the posterior probability is higher for apples hence they are assigned to the apple class" \
        "and to the right oranges"):
            boundary = DashedLine(
                self.nl.c2p(0.65, -1),
                self.nl.c2p(0.65, 4),
                color=WHITE
            )

            self.play(Create(boundary))

        with self.voiceover("well what about the parts of the graph that cross over to the other side of the boundary") as tracker:
            def area_under(axes, fn, x_min, x_max, color, n=100):
                xs = np.linspace(x_min, x_max, n)
                points = [axes.c2p(x, fn(x)) for x in xs]
                # close the polygon down to the axis
                points.append(axes.c2p(x_max, 0))
                points.append(axes.c2p(x_min, 0))
                poly = Polygon(*points, color=color, fill_opacity=0.4, stroke_width=0)
                return poly

            apple_post_fn = lambda x: 0.5 * apple_pdf(x)
            orange_post_fn = lambda x: 0.5 * orange_pdf(x)

            x_cross = (mu_apple + mu_orange) / 2  # 0.65

            apple_error = area_under(self.nl, apple_post_fn, x_cross, 1.0, RED)
            orange_error = area_under(self.nl, orange_post_fn, 0.3, x_cross, ORANGE)

            apple_error.set_fill(RED, opacity=0.4)
            orange_error.set_fill(ORANGE, opacity=0.4)

            apple_error.set_stroke(width=0)
            orange_error.set_stroke(width=0)


            self.play(
                FadeIn(apple_error),
                FadeIn(orange_error)
            )

        with self.voiceover("these show the error in our boundary and if we add these up we get the classification error"):
            add = Tex("+")
            eq = Tex("=")
            clas = Tex("Classification Error")
            self.play(
            orange_error.animate.scale(0.5).move_to(UP * 3 + RIGHT)
            )

            add = Tex("+").scale(0.5).next_to(orange_error, RIGHT)
            apple_error.scale(0.5).next_to(add, RIGHT)
            eq.scale(0.5).next_to(apple_error, DOWN + LEFT)
            clas.scale(0.5).next_to(eq, RIGHT)

            self.play(
                FadeIn(add),
                FadeIn(apple_error),
                FadeIn(eq),
                FadeIn(clas),
            )

        with self.voiceover("The Bayes error is the smallest classification error achievable and it tells us the theoretical limit of how well the two classes can be separated.") as tracker:
            self.wait(tracker.duration)

        