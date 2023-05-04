import pygame
import random
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
        [np.array([0, 1, 4, 8, 2]), np.array([0, 4, 5, 6, 3]), np.array([1, 5, 9, 8, 2]), np.array([4, 5, 6, 10, 3])],
        [np.array([0, 1, 5, 9, 2]), np.array([4, 5, 6, 8, 3]), np.array([0, 4, 8, 9, 2]), np.array([2, 4, 5, 6, 3])],
        [np.array([1, 4, 5, 6, 3]), np.array([1, 4, 5, 9, 2]), np.array([4, 5, 6, 9, 3]), np.array([0, 4, 5, 8, 2])],
        [np.array([0, 1, 4, 5, 2])],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
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

        self.height = height
        self.width = width
        self.field = np.zeros((height, width))
        self.score = 0
        self.state = "start"

    def new_figure(self):
        self.figure = Figure(0, 0)

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

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def test_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        return self.test_freeze()

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

    def test_freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y < 0 or i + self.figure.y >= self.height \
                       or j + self.figure.x < 0 or j + self.figure.x >= self.width:
                        return False
                    self.field[i + self.figure.y][j +
                                                  self.figure.x] = self.figure.color
                    
        return True

    # difference between max height column and min height column
    def bumpiness(self):
        min_col = self.height
        max_col = 1
        for i in range(self.width):
            h = 0
            while(h < self.height):
                if(self.field[h][i] != 0):
                    break
                h += 1
            min_col = min(min_col, h)
            max_col = max(max_col, h)
        return max_col - min_col

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
            while(h < self.height):
                if(self.field[h][i] != 0):
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
            while(h < self.height):
                if(self.field[h][i] != 0):
                    break
                h += 1
            heights.append(h)
        for i in range(self.width):
            for j in range(1, self.height):
                if(self.field[j][i] == 0 and j > heights[i]):
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

        self.figure = Figure(0, 0)
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
                if(possible):
                    curr_score = param1 * background.aggregate_height() + param2 * background.bumpiness() 
                    + param3 * background.complete_lines() + param4 * background.holes()
                    if(curr_score >= max_score):
                        max_score = curr_score
                        best_move = [j, i]
        
        self.figure.rotate(best_move[1])
        self.figure.x = best_move[0]
        self.go_space()

def trainingGame(param1, param2, param3, param4, rounds, moves):
    list = []
    for i in range(rounds):
        game = Tetris(20, 10)
        game.new_figure()
        for j in range(moves):
            if game.state == "gameover":
                break
            game.best_moves(param1, param2, param3, param4)
        list.append(game.score)
    return list

print(trainingGame(-1, -1, 1, -1, 10, 100))
        
