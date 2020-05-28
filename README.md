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

    Short video with functionality of the program: https://youtu.be/BeXnsyBBVoo

    This task was based on a book published by Raymond Smullyan in 1978 called "What is the name of this book". It's a book of logical puzzles and one of them is called "Knights and Knaves". 

    Considering the contrains of the puzzle which assume that Knights always tell the truth and Knaves always lie, I wrote a program that finds out who is a kinght and who is knave based on what the people said. 

    The task involved manipulating with built structures in Python such as Implication, Or and And operators. 

    The 'intelligent' part of the program was based on the idea of inferences. That the program, given a couple of initial constrains and facts, can infere some new assumptions from them.

    Full description can be found at: https://cs50.harvard.edu/ai/2020/projects/1/knights/

    2. Minesweeper

    Video with functionality: https://youtu.be/f4u2wQyHCYU

    This task was to implement a well-known game "Minesweeper" in a way that the computer will play it. 

    This is another example of idea of working with inferences. Computer, given some initial variables, will infer which fields are safe and he will choose them next. 

    Some of the ways how to infere new assumptions are following:
        - if we have a cell with number 0, we can infere that there is no bomb in any surrounding cell,
        - if the number of surrounding cells that are not safe is equal to the number on the cell it means that all the cells have a bomb.

    Based on logical assumptions like those, AI can recursively try infere new information about the board. 

    Full description can be found at: https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/

WEEK 2

Tasks: "PageRank", "Heredity"

    1. PageRank

    This week's tasks are based on the idea of AI which needs to make unsure decisions. The way how to work with those situations is taking into account theory of Probability.

    In the PageRank task, I wrote a program which ranks web-pages by importance. The algorithms I used were Random Surfer model, where a random user is considered who clicks on the links at random. Therefore, the more links to a certain page, the higher probability the surfer will end up there. 

    Since this algorithm is not functioning well if all the webpages are not connected (are not forming one graph but more), I used as well the Iterative algorithm. 

    Full description at: https://cs50.harvard.edu/ai/2020/projects/2/pagerank/

    2. Heredity

    