import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
import copy

class MCTS(VoiceoverScene):

    def construct(self):

        self.set_speech_service(RecorderService(transcription_model=None))
        self.intro()
        self.example()

    def make_x(self, position):

        x1 = Line(
            position + 0.3 * UP + 0.3 * LEFT,
            position + 0.3 * DOWN + 0.3 * RIGHT
        )

        x2 = Line(
            position + 0.3 * UP + 0.3 * RIGHT,
            position + 0.3 * DOWN + 0.3 * LEFT
        )

        return VGroup(x1, x2)

    def intro(self):

        with self.voiceover("in 2016, a computer program called alpha go defeated the world champion Lee sedol" \
        "in a board game called go"):
            alpha = ImageMobject("image.png").move_to(LEFT * 3).scale(0.5)
            lee = ImageMobject("lee.png").move_to(RIGHT * 2).scale(0.5)
            self.play(FadeIn(alpha))
            self.wait(1)
            self.play(FadeIn(lee))

        with self.voiceover("but how can a computer actually know which move is the best one to be played?"):
            ques = Tex("?")
            self.play(FadeIn(ques))

        self.remove(alpha, lee, ques)

        with self.voiceover("the algorithm alpha go used was called MCTS"):
            acr = Tex("M", "C", "T", "S")
            full = Tex("M", "onte ", "C", "arlo ", "T", "ree ", "S", "earch")
            acr.move_to(UP * 3)
            full.move_to(UP * 3)
            self.play(Write(acr))

        with self.voiceover("or monte carlo tree search"):
            self.play(TransformMatchingTex(acr, full, transform_mismatches=True))

        with self.voiceover("well actually it used a more complex version of this algorithm but lets explore the basic idea with a game of tic tac toe.") as tracker:
            self.play(full.animate.move_to(UP * 3.2).scale(0.8))

        self.wait(2)

    def example(self):

        with self.voiceover("say the tic tac toe board looks like this and it is the computers turn to make a move"):

            main_board = self.make_board({(0, 0) : 'X', (2, 2) : 'O'})
            self.play(Create(main_board))

        with self.voiceover("the computer stores the current position and paths it has explored in a tree format"):

            configs = {
                "root" : {(0, 0) : 'X', (2, 2) : 'O'},
                "left" : {(0, 0) : 'X', (1, 1) : 'X', (2, 2) : 'O'},
                "right" : {(1, 0) : 'X', (0, 1) : 'X', (2, 2) : 'O'},
                "left_left" : {(0, 0) : 'X', (1, 1) : 'X', (2, 2) : 'O', (2, 0) : 'O'},
                "left_right" : {(0, 0) : 'X', (1, 1) : 'X', (2, 2) : 'O', (1, 0) : 'O'}
            }

            edges = [
                ("root", "left", "P(X, center, center)"),
                ("root", "right", "P(X, left, center)"),
                ("left", "left_left", "P(O, left, bottom)"),
                ("left", "left_right", "P(O, left, center)")
            ]

            positions = {
                    "root": UP * 2.2,
                    "left": UP * 0.3 + LEFT * 3.2,
                    "right": UP * 0.3 + RIGHT * 3.2,
                    "left_left": DOWN * 2.2 + LEFT * 5.3,
                    "left_right" : DOWN * 2.2 + LEFT * 0.8,
                }

            captions = {
                "root": "Value : 0.4",
                "left": "Value : 0.5",
                "right": "Value : 0.3",
                "left_left": "Value : 0.7",
                "left_right" : "Value : 0.3"
            }

            nodes = {}
            boards = VGroup()
            for name, cfg in configs.items():
                board = self.make_board(cfg).scale(0.32)
                board.move_to(positions[name])
                nodes[name] = board
                boards.add(board)

            edge_lines = VGroup()
            edge_labels = VGroup()
            for a, b, text in edges:
                line = self.connect(nodes[a], nodes[b])
                edge_lines.add(line)
    
                label = Text(text, font_size=16)
                label.move_to(line.get_center())
                bg = BackgroundRectangle(label, fill_opacity=1, buff=0.05)
                edge_labels.add(VGroup(bg, label))
    
            board_captions = VGroup()
            for name, board in nodes.items():
                caption = Text(captions[name], font_size=16)
                caption.next_to(board, DOWN, buff=0.15)
                board_captions.add(caption)

            self.play(ReplacementTransform(main_board, boards[0]))
            self.play(Create(edge_lines), *[Create(b) for b in boards[1:]])
            self.play(Write(edge_labels), Write(board_captions))
            self.wait()

        with self.voiceover("on the branches between does, we see the transition function, which tells the result of performing " \
        "an action of a state") as tracker:
            self.wait(tracker.duration)

        with self.voiceover("for example this one means putting an X on the center left square"):
            self.play(edge_labels[1][1].animate.scale(1.3).set_color(YELLOW))

        self.play(edge_labels[1][1].animate.scale(1 / 1.3).set_color(WHITE))

        with self.voiceover("the value under the node tells us how favourable a specific path, right now"):
            self.play(board_captions[1].animate.scale(1.3).set_color(YELLOW))

        self.play(board_captions[1].animate.scale(1/1.3).set_color(WHITE))

        with self.voiceover("we first start with selection, where starting from the root, we select a child node" \
        "until we reach one that hasnt been fully expanded, the way we select a particular node is called a " \
        "heuristic") as tracker:
            self.play(Indicate(boards[0], scale_factor=1.2), run_time=3)
            self.play(Indicate(edge_lines[1][0], color=YELLOW), run_time=3)
            self.play(Indicate(boards[2], scale_factor=1.2, color=YELLOW), run_time=tracker.duration - 6)

        with self.voiceover("lets say we want to see what happens when we put an O on the top right"):
            new_board = self.make_board({(1, 0) : 'X', (0, 1) : 'X', (2, 2) : 'O', (0, 2) : 'O'}).scale(0.32)
            new_board.move_to(DOWN * 1.5 + RIGHT * 5.2)
            boards.add(new_board)
            nodes['right_left'] = new_board
            new_line = self.connect(nodes['right'], nodes['right_left'])
            edge_lines.add(new_line)
            new_label = Text('P(O, right, top)', font_size=16)
            new_label.move_to(new_line.get_center())
            new_bg = BackgroundRectangle(new_label, fill_opacity=1, buff=0.05)
            edge_labels.add(VGroup(new_bg, new_label))
            caption = Text('Value : N/A', font_size=16)
            caption.next_to(new_board, DOWN, buff=0.15)
            board_captions.add(caption)
            self.play(
                Create(new_board),
                Create(new_line),
                Write(new_bg),
                Write(new_label),
                Write(caption)
            )


        with self.voiceover("we want to find out that if we made this move, would we win or not, so we run a simulation," \
        "where we play out a bunch of games, with randomised moves till we have reached a terminating state, in this case " \
        "either a loss or a win"):
            arr = Arrow(
                start=new_board.get_bottom() + DOWN * 0.4,
                end=new_board.get_bottom() + DOWN * 0.9,
                buff=0
            )
            sim_text = Text(
                "Simulation",
                font_size=16
            ).next_to(arr, RIGHT, buff=0.15)

            self.play(
                Create(arr),
                Write(sim_text)
            )

        with self.voiceover("say in our first simulation we got a win"):
            win = Text(
                "Win!",
                font_size=16,
                color=GREEN
            ).next_to(arr, DOWN, buff=0.2)

            self.play(Write(win))

        with self.voiceover("this is good but it isnt reliable to believe just one simulation so we do multiple simulations") as tracker:
            self.wait(tracker.duration)

        with self.voiceover("lets say out of 100 simulations, we won 75 of them"):
            results = VGroup(
                Text("100 simulations", font_size=16),
                Text("75 wins", font_size=16)
            ).arrange(DOWN, buff=0.08)

            results.move_to(win.get_center())

            self.play(ReplacementTransform(win, results))

        with self.voiceover("great we can then write the value or reward of this node as 0.75"):
            n_caption = Text(
                "Value : 0.75",
                font_size=16
            ).move_to(caption.get_center())

            self.play(
                ReplacementTransform(caption, n_caption)
            )

            self.play(
                Indicate(n_caption, scale_factor=1.2)
            )

        print(edge_labels)
        print(edge_lines)
        print(boards)
        with self.voiceover("so we know that if we make this action we get a reward of 0.75") as tracker:
            self.wait(tracker.duration)

        with self.voiceover("lets tell the nodes above it in the path this so they can update their values, this is called back propogation"):
            self.play(Indicate(new_line, color=YELLOW))
            old_cap = board_captions[2]
            n_val_1 = Text("Value : 0.525", font_size=16).move_to(old_cap.get_center())
            self.play(ReplacementTransform(old_cap, n_val_1))
            self.play(Indicate(n_val_1))

            self.play(Indicate(edge_lines[1][0], color=YELLOW))
            old_cap = board_captions[0]
            n_val_2 = Text("Value : 0.5125", font_size=16).move_to(old_cap.get_center())
            self.play(ReplacementTransform(old_cap, n_val_2))
            self.play(Indicate(n_val_2))

        with self.voiceover("great so we explored a new move and if we compare this path and the other we can see that the reward" \
        "for the right path is higher than the other so the computer should favour this move"):
            self.wait(2)
            self.play(Indicate(board_captions[1], color=YELLOW), run_time = 2)
            self.play(Indicate(board_captions[2], color=YELLOW), run_time = 2)

        with self.voiceover("keep in mind, real implementations don't just look at winrate but also factor in how many times a path" \
        "has actually been explored, since a node we've only tried once could just a lucky win") as tracker:
            self.wait(tracker.duration) 

        with self.voiceover("in theory, the computer would compute these values for all possible moves but since we dont have that " \
        "much time and computer power the computer needs to balance exploring untried moves with exploiting the moves we already know are promising") as tracker:
            self.wait(tracker.duration)

        with self.voiceover("this is called the exploration-exploitation tradeoff, and it shows up everywhere in reinforcement learning not just MCTS"):
            ee = Tex("Exploration - Exploitation Tradeoff")
            self.clear()
            self.play(Write(ee))




    


    def make_board(self, state=None, board_size=1.5, mark_scale=0.35, color=WHITE):
        state = state or {}
        board = VGroup()

        for x in [-0.5, 0.5]:
            board.add(Line(UP * board_size + RIGHT * x, DOWN * board_size + RIGHT * x, color=color))
        for y in [-0.5, 0.5]:
            board.add(Line(LEFT * board_size + UP * y, RIGHT * board_size + UP * y, color=color))

        cell_centers = {
            (row, col): np.array([(col - 1) * 1.0, (1 - row) * 1.0, 0.0])
            for row in range(3)
            for col in range(3)
        }

        for (row, col), mark in state.items():
            center = cell_centers[(row, col)]
            if mark == "X":
                board.add(self.make_x(center, mark_scale))
            elif mark == "O":
                board.add(self.make_o(center, mark_scale))

        return board

    def make_x(self, center, scale=0.35, color=RED):
        x_mark = VGroup(Line(UL, DR, color=color), Line(UR, DL, color=color)).scale(scale)
        x_mark.move_to(center)
        return x_mark


    def make_o(self, center, scale=0.35, color=BLUE):
        o_mark = Circle(radius=1, color=color).scale(scale)
        o_mark.move_to(center)
        return o_mark


    def connect(self, node_a, node_b, color=WHITE, stroke_width=2, buff=0.15):
        
        direction = node_b.get_center() - node_a.get_center()
        start = node_a.get_boundary_point(direction)
        end = node_b.get_boundary_point(-direction)
        return Line(start, end, color=color, stroke_width=stroke_width, buff=buff)
            

