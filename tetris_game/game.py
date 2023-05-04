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
        self.rotation = 0
        self.width = self.figures[self.type][self.rotation][4]

    def image(self):
        return self.figures[self.type][self.rotation][:4]

    def rotate(self, r):
        self.rotation = r


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
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

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

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self, r):
        old_rotation = self.figure.rotation
        self.figure.rotate(r)
        if self.intersects():
            self.figure.rotation = old_rotation

    # Need to create: bumpiness, complete lines, aggregate height, holes, next_states
    def bumpiness(self):
        min_col = self.height
        max_col = 1
        for i in range(self.width):
            h = self.height
            while(h>1):
                if(self.field[i][h] != 0):
                    break
                h -= 1
            min_col = min(min_col, h)
            max_col = max(max_col, h)
        return max_col - min_col

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
    
    def aggregate_height(self):
        agg_height = 0
        for i in range(self.width):
            h = self.height
            while(h>1):
                if(self.field[i][h] != 0):
                    break
                h -= 1
            agg_height += h
        return agg_height
    
    def holes(self):
        heights = []
        holes = 0
        for i in range(self.width):
            h = self.height
            while(h>1):
                if(self.field[i][h] != 0):
                    break
                h -= 1
            heights.append(h)
        for i in range(self.width):
            for j in range(1, self.height):
                if(self.field[i][j] == 0 and j < heights[i]):
                    holes += 1
        return holes
        





# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [
                             game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[int(game.field[i][j])],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom *
                                      (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()