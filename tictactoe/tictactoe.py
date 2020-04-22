"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0

    # Go through the board counting X and O
    for row in board:
        for col in row:
            if col == O:
                countO+=1
            if col == X:
                countX+=1

    # Return X if it is the first move
    if countX == 0 and countO == 0:
        return X
    # otherwise if X has one more than O, return O
    elif countX-countO == 1:
        return O
    # otherwise return X
    else:
        return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actns = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actns.add((i, j))
    return actns
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Raise an error in case of invalid action 
    for a in action:
        if a not in (0,1,2):
            raise NameError("Action out of board")
    if board[action[0]][action[1]] != EMPTY:
        raise NameError("Field already taken")
    
    currentPlayer = player(board)
    newBoard = copy.deepcopy(board)
    newBoard[action[0]][action[1]] = currentPlayer

    return newBoard
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Initializing all possible win combinations
    h0 = board[0][0]
    v0 = board[0][0]
    d0 = board[0][0]
    d1 = board[0][2]
    v1 = board[0][1]
    v2 = board[0][2]
    h1 = board[1][0]
    h2 = board[2][0]

    possibleWins = {(d0,0), (h0,1), (h1,2), (h2,3), (v0,4), (v1,5), (v2,6), (d1,7)}

    # check for diagonal d1, because it doesn't fit into below loop
    if board[0][2] != board[1][1] or board[1][1] != board[2][0]:
        possibleWins.discard((d1,7))

    # Check all the other options
    for i in range(1,3):
        if board[i][i] != board[i-1][i-1]:
            possibleWins.discard((d0,0))
        if board[i][0] != board[i-1][0]:
            possibleWins.discard((v0,4))
        if board[i][1] != board[i-1][1]:
            possibleWins.discard((v1,5))
        if board[i][2] != board[i-1][2]:
            possibleWins.discard((v2,6))
        if board[0][i] != board[0][i-1]:
            possibleWins.discard((h0,1))
        if board[1][i] != board[1][i-1]:
            possibleWins.discard((h1,2))
        if board[2][i] != board[2][i-1]:
            possibleWins.discard((h2,3))
    if len(possibleWins) == 0:
        return None
    else:
        win = possibleWins.pop()
        return win[0]

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        for col in row:
            if col == EMPTY:
                return False
    return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return maxValue(board)
    else:
        return minValue(board)

    raise NotImplementedError

def minValue(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v

def maxValue(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v