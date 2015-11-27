# Conway's game of life

from random import randint
from time import sleep
from copy import deepcopy

# updates the board according to the four rules
def newCycle(board):
    # create a duplicate of the board to update
    new = deepcopy(board)
    for y in range(boardSize):
        for x in range(boardSize):
            n = countLiveNeighbours(board, x, y)
            # activates cells with three neighbours
            if board[y][x] == ' ' and n == 3:
                new[y][x] = 'X'
            # kills over- or underpopulated cells
            elif board[y][x] == 'X' and (n < 2 or n > 3):
                new[y][x] = ' '
    return new, board

# why does this need a deepcopy to work? I thought it would be okay just altering board locally
def printBoard(display, history):
    for y in range(boardSize):
        for x in range(boardSize):
            if display[y][x] == 'X':
                if history[-1][y][x] == ' ':
                    display[y][x] = g['newborn']
                else:
                    display[y][x] = g['live']
            elif display[y][x] == ' ':
                if history[-1][y][x] == 'X':
                    display[y][x] = g['dying']
                else:
                    display[y][x] = g['dead']
    print('\n'.join([''.join(x) for x in display]) + '\n' + '_'*boardSize)
                

# Counts the number of neighbours of a cell that are alive
def countLiveNeighbours(board, x, y):
    l = [(y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)] 
    neighbours = []
    for i in l:
        try:
            if i[0] != -1 and i[1] != -1:
                neighbours.append(board[i[0]][i[1]])
            else:
                raise IndexError
        except IndexError:
            neighbours.append(' ')
    return neighbours.count('X')
    

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
            

### SETTINGS ###

maxGenerations = 100 # max number of generations that the game will run for
boardSize = 25 # length of each side of the board (board is a square)
maxPopulation = (boardSize**2)//1.25 # max number of initial live cells (default 80% of board)
minPopulation = (boardSize**2)//10 # minimum number of initial live cells (default 10% of board)
sleepTime = 0.2 # time in seconds between each update of the board
graphics = g = {'live':'X', 'dead':' ','newborn':'x', 'dying':'-'} # characters used for each cell state

### INITIALISATIONS ###

# initialise the board to a blank grid
board = [list(' '*boardSize) for x in range(boardSize)] # board as a list of lists, can use [y][x] as a co-ordinate ref

# populate the board with a random number of live cells in random positions
for i in range(randint(minPopulation, maxPopulation)):
    (y, x) = randint(0, boardSize - 1), randint(0, boardSize - 1)
    board[y][x] = 'X'
'''
# oscillator test
for f in range(3):
    board[2][f] = 'X'
'''
# initialise the count of generations, and the history, which is used to detect oscillators  
generations = 0
history = []

### MAIN LOOP ###

while generations < maxGenerations:
    if generations > 1:
        printBoard(deepcopy(board), history) 
    board, oldBoard = newCycle(board)
    if board == oldBoard:
        print('Static')
        break
    history.append(oldBoard)
    if checkOscillation(history, board) == 0:
        print('Oscillator reached')
        break
    sleep(sleepTime)
    generations += 1
