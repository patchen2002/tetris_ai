# Tetris AI
<img src="https://github.com/patchen2002/tetris_ai/blob/main/tetris_sc.png" width="1000" />

Created in May 2023

### Members

- Patrick Chen
- Corwin Zhang
- Aurora Mu

### Description

This Tetris AI is trained to clear as many lines as possible. At each step, there is a function best_moves that determines what the best move is given a gamestate. We used a genetic algorithm to find out which parameters would let this bot clear the most number of lines. Current high score is 1856 lines.


## How to Run
Requirements: Python and Pygame

1. Clone this repository
2. Navigate into the tetris_game directory
3. If you want to run our AI model to simulate a new set of parameters
    - Open the trainingAlgorithm.py file
    - On the last line, find the trainingAlgorithm.training function.() It should have three parameters. These parameters are, in order: number of bots, number of games, and maximum number of moves per game. Fill in whatever numbers you want
    - Run the command `python3 trainingAlgorithm.py`. Every iteration, it should print out information about the fitness and what the best parameters were
4. If you want to watch the bot at work
    - Open the game.py file and go to line 83. There, you can fill in the four parameters you got from step three(or leave them as is). The order of the parameters is: aggregate height, bumpiness, complete lines, and holes
    - Run the command `python3 game.py`
    - A Tetris GUI should pop up and you can watch the game play out
