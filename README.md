CS50’s
Introduction to Artificial Intelligence with Python


This the coursework from an online course I pursued through edx platform of the above title. The course focuses on introduction to AI concepts such as Machine Learning and Neural Networks. I will be posting here my progress throughout the course. The more detialed description and further information is on the website of the course: https://cs50.harvard.edu/ai/.

I will be gradually updating this readme file with descriptions of each weekly assignment.

WEEK 0

Tasks: "Degrees", "Tic-Tac-Toe"
    
    1. Degrees

    I uploaded a short video that presents the functionality of the program at: https://youtu.be/WwaMH1LRgZQ
    
    The task involve using Breadth-search first (BFS) in order to find the corresponding path from one actor to another according to theory of Six Degrees of Kevin Bacon. 

    Example and full description of the task can be found on: https://cs50.harvard.edu/ai/projects/0/degrees/

    2. TicTacToe

    I uploaded a short video that presents the functionality of the program at: https://youtu.be/2SVmOkVgqpw
    
    This task involved implementing a basic AI that would play a tic-tac-toe with you. The AI will always pick the best option which results in the fact that you can't win the game. 

    The problem involves implementing a search algorithm, that AI can use in order to find the best solution or an optimal one if there is no clear distinguishing feature between them. 

    The task involved implementing several functions such as player, actions, result, winner, terminal, utility and minimax. The main search algorithm runs in minimax, where I implemented it with the idea of Alpha-Beta Pruning. This is an optimazation which provides that the AI will not search through all the possible solutions but rather until it finds the best one. 

    The idea of an algorithm, in short can be desribed in a following way: The X player wants to maximize the result and the O player wants to minimize it. In this way, we represent a winning-X board game with a 1 and winning-O game with -1. The tie board game would be 0. During the game the AI will recursively try all the possible moves that can be made, and after each move it will consider what its oponent would do in the next move. This logic is implemented in the minimax function. The Alpha-Beta pruning optimazation of course provides that the AI won't always go through all the possible moves. 

    Full description of the task can be found at: https://cs50.harvard.edu/ai/projects/0/tictactoe/
    
WEEK 1

Tasks: "Knigths", "Minesweeper"

    1. Knights

    2. Minesweeper

WEEK 2

Tasks: "PageRank", "Heredity"

    1. PageRank

    2. Heredity