import pygame
import random
import ai
import numpy as np
# testing
colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:
    x = 0
    y = 0

    figures = [
        [np.array([0, 4, 8, 12, 1]), np.array([0, 1, 2, 3, 4])],
        [np.array([4, 5, 9, 10, 3]), np.array([1, 5, 4, 8, 2])],
        [np.array([5, 6, 8, 9, 3]), np.array([0, 4, 5, 9, 2])],
        [np.array([0, 1, 4, 8, 2]), np.array([0, 4, 5, 6, 3]),
         np.array([1, 5, 9, 8, 2]), np.array([4, 5, 6, 10, 3])],
        [np.array([0, 1, 5, 9, 2]), np.array([4, 5, 6, 8, 3]),
         np.array([0, 4, 8, 9, 2]), np.array([2, 4, 5, 6, 3])],
        [np.array([1, 4, 5, 6, 3]), np.array([1, 4, 5, 9, 2]),
         np.array([4, 5, 6, 9, 3]), np.array([0, 4, 5, 8, 2])],
        [np.array([0, 1, 4, 5, 2])],
    ]

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.color = random.randint(1, len(colors) - 1)
        self.forms = len(self.figures[self.type])
        self.rotation = 0
        self.width = self.figures[self.type][self.rotation][4]

    def image(self):
        return self.figures[self.type][self.rotation][:4]

    def rotate(self, r):
        self.rotation = r
        self.width = self.figures[self.type][self.rotation][4]

    def clone(self, og):
        self.x = og.x
        self.y = og.y
        self.type = og.type
        self.color = og.color
        self.forms = og.forms
        self.rotation = og.rotation
        self.width = og.width


class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
        self.cycle = random.sample(range(0, 7), 7)
        self.curr_figure = 0

        self.height = height
        self.width = width
        self.field = np.zeros((height, width))
        self.score = 0
        self.state = "start"

    def new_figure(self):
        self.figure = Figure(0, 0, self.cycle[self.curr_figure])
        self.curr_figure += 1
        if(self.curr_figure > 6):
            self.curr_figure = 0
            self.cycle = random.sample(range(0, 7), 7)

    # checks if the piece is out of the board or filling up another piece
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    # check if any lines are full and breaks them
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines

    # moves the block down as far as it can go
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    # simulates moving the block down to the furthest it goes
    def test_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        return self.test_freeze()

    # checks to see if there are any intersections, breaks lines, and fills in the board
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j +
                                                  self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    # fills out the board and checks if the block is out of the board limits
    def test_freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y < 1 or i + self.figure.y >= self.height \
                       or j + self.figure.x < 0 or j + self.figure.x >= self.width:
                        return False
                    self.field[i + self.figure.y][j +
                                                  self.figure.x] = self.figure.color

        return True

    # difference between adjacent column
    def bumpiness(self):
        heights = []
        bumpiness = 0
        for i in range(self.width):
            h = 0
            while(h < self.height):
                if(self.field[h][i] != 0):
                    break
                h += 1
            heights.append(h)
        
        for i in range(len(heights)-1):
            bumpiness += abs(heights[i] - heights[i+1])
        return bumpiness

    # determines how many lines are complete
    def complete_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
        return lines

    # total height
    def aggregate_height(self):
        agg_height = 0
        for i in range(self.width):
            h = 0
            while (h < self.height):
                if (self.field[h][i] != 0):
                    break
                h += 1
            agg_height += self.height - h
        return agg_height

    # how many squares are under blocks
    def holes(self):
        heights = []
        holes = 0
        for i in range(self.width):
            h = 0
            while (h < self.height):
                if (self.field[h][i] != 0):
                    break
                h += 1
            heights.append(h)
        for i in range(self.width):
            for j in range(1, self.height):
                if (self.field[j][i] == 0 and j > heights[i]):
                    holes += 1
        return holes

    # creates a copy of the gamestate
    def clone(self, og):
        self.level = og.level
        self.score = og.score
        self.state = og.state
        self.field = og.field.copy()
        self.height = og.height
        self.width = og.width
        self.x = og.x
        self.y = og.y
        self.zoom = og.zoom

        self.figure = Figure(0, 0, 0)
        self.figure.clone(og.figure)

    # for a given gamestate and figure, figures out the best possible move for every rotation and location
    def best_moves(self, param1, param2, param3, param4):
        forms = self.figure.forms
        background = Tetris(20, 10)
        background.clone(self)
        curr = background.figure
        max_score = -1000000
        best_move = [0, 0]

        for i in range(forms):
            curr.rotate(i)
            for j in range(background.width - curr.width + 1):
                background.field = self.field.copy()
                curr.x = j
                curr.y = 0
                possible = background.test_space()
                if (possible):
                    curr_score = param1 * background.aggregate_height() + param2 * \
                        background.bumpiness()
                    + param3 * background.complete_lines() + param4 * background.holes()
                    if (curr_score >= max_score):
                        max_score = curr_score
                        best_move = [j, i]

        self.figure.rotate(best_move[1])
        self.figure.x = best_move[0]
        self.go_space()

# takes in an array of AI objects, simulates the game with their parameter a certain number of rounds up to a certain number of moves


def computeFitness(AIList, rounds, moves):
    for ai in AIList:
        fitness = 1
        for i in range(rounds):
            game = Tetris(20, 10)
            game.new_figure()
            for j in range(moves):
                game.best_moves(ai.heightWeight, ai.bumpinessWeight,
                                ai.linesWeight, ai.holesWeight)
                if game.state == "gameover":
                    break
            fitness += game.score
        # print("fitness", fitness)
        ai.fitness = fitness/rounds

def computeFitnessTest(p1, p2, p3, p4, rounds, moves):
    list = []
    for i in range(rounds):
        game = Tetris(20, 10)
        game.new_figure()

        for j in range(moves):
            game.best_moves(p1, p2, p3, p4)
            if game.state == "gameover":
                break
        list.append(game.score)
    return list

