# Conway's game of life

import random
import time

# print the generation and then update the board [could really just add this to main loop]
def printBoard(board):
    print(''.join(board))
    board = newCycle(board)
    return board

# updates the board according to the four rules
def newCycle(board):
    # create a duplicate of the board to update
    new = list(board)
    for i in range(len(board)):
        if board[i] == '\n':
            continue
        else:
            n = countLiveNeighbours(board, i)
            # activates cells with three neighbours
            if board[i] == ' ' and n == 3:
                new[i] = 'X'
            # kills over- or underpopulated cells
            elif n < 2 or n > 3:
                new[i] = ' '
    return new, board

def countLiveNeighbours(board, i):
    # generates a list of neighbours, including blanks for any off-board cells. Format [NW, N, NE, W, E, SW, S, SE]
    if i < 1:
        neighbours = [' ', ' ', ' ', ' ', board[i + 1], ' ', board[i + 31], board[i + 32], 'top left']
    elif i < 31:
        neighbours = [' ', ' ', ' ', board[i - 1], board[i + 1], board[i + 30], board[i + 31], board[i + 32], 'first row']
    elif i < len(board) - 31:
        neighbours = [board[i - 32], board[i - 31], board[i - 30], board[i - 1], board[i + 1], board[i + 30], board[i + 31], board[i + 32], 'main']
    elif i == len(board) - 31:
        neighbours = [' ', board[i - 31], board[i - 30], ' ', board[i + 1], ' ', ' ', ' ', 'bottom left'] 
    else:
        neighbours = [board[i - 32], board[i - 31], board[i - 30], board[i - 1], board[i + 1], ' ', ' ', ' ', 'last row']
    n = 0
    for j in neighbours:
        if j == 'X':
            n += 1
# debug statement   print(str(i) + ' ' + str(neighbours) + ' ' + str(n))
    return n

# checks to see if the board is in an oscillating state 
def checkOscillation(history, board):
    oscillationRange = 10
    # limits the length of history to the maximum length the oscillator check will look at
    while len(history) > 2*oscillationRange:
        del history[0]
    for i in range(1, oscillationRange):
        if len(history) < 2*i:
            break
        elif board == history[-i] == history[-2*i]:
            return 0
            

# initialise the board to a blank grid
board = list((' ' * 30 + '\n') * 30)

'''
# oscillator test - toad (de-activate random populator before use):
board[42] = 'X'
board[43] = 'X'
board[44] = 'X'
board[54] = 'X'
board[55] = 'X'
board[56] = 'X'
'''

# populate the board with a random number of live cells in random positions
for i in range(random.randint(0, 300)):
    index = random.randint(0, 929)
    if board[index] == '\n':
        continue
    else:
        board[index] = 'X'

# initialise the count of generations and execute the main loop   
generations = 0
history = []

while generations < 100: # manually enter no. of generations here
    board, oldBoard = printBoard(board)
    if board == oldBoard:
        print('Static')
        break
    history.append(oldBoard)
    if checkOscillation(history, board) == 0:
        print('Oscillator reached')
        break
    time.sleep(0.1) # enter the time taken for each generation here
    generations += 1

