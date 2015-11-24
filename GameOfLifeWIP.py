# Conway's game of life

from random import randint
from time import sleep
from copy import deepcopy

'''
# UPDATED FOR NEW BOARD  ----  MOVED INTO MAIN LOOP
# print the generation and then update the board [could really just add this to main loop]
def printBoard(board):
    print('\n'.join([''.join(x) for x in board]))
    return newCycle(board)
'''

# UPDATED BUT NEEDS TESTING --- Currently board is updating as well as new in the if/elif statements
# updates the board according to the four rules
def newCycle(board):
    # create a duplicate of the board to update
    new = deepcopy(board) # similar issue to before has occurred where calling new will update board
    for y in range(boardSize):
        for x in range(boardSize):
            n = countLiveNeighbours(board, x, y)
            #print('   n = ' + str(n))
            # activates cells with three neighbours
            #print(str(y) + ', ' + str(x) + ', ' + str(n) + ', "' + str(board[y][x]) + '"', end = '')
            if board[y][x] == ' ' and n == 3:
                #print(" come alive", end = ' ')
                new[y][x] = 'X'
                #print(board[y][x], end = '')
                #print(new[y][x], end = '')
            # kills over- or underpopulated cells
            elif n < 2 or n > 3:
                #print(" die", end = '')
                new[y][x] = ' '
                #print(board[y][x], end = '')
                #print(new[y][x], end = '')
            #print('')
    return new, board

          
# UPDATED BUT NEEDS TESTING Also check that when called, it provides both x and y (previously provided a single arg)
# the -1 causes index 0 to wrap around and check the end of the string, fix this
def countLiveNeighbours(board, x, y):
    l = [(y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)] 
    neighbours = []
    for i in l:
        try:
            if i[0] != -1 and i[1] != -1:
                neighbours.append(board[i[0]][i[1]])
                #print('"' + str(board[i[0]][i[1]]) + '"', end = '')
            else:
                raise IndexError
        except IndexError:
            neighbours.append(' ')
            #print('" "', end = '')
    return neighbours.count('X')
    

# DON'T THINK AN UPDATE IS REQUIRED
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
            

# SETTINGS

maxGenerations = 100 # max number of generations that the game will run for
boardSize = 30 # length of each side of the board (board is a square)
maxPopulation = 300# max number of initial live cells
minPopulation = 100 # minimum number of initial live cells

# UPDATED FOR NEW BOARD
# initialise the board to a blank grid
board = [list(' '*boardSize) for x in range(boardSize)] # board as a list of lists, can use [y][x] as a co-ordinate ref

# UPDATED BUT NEEDS TESTING
# populate the board with a random number of live cells in random positions
for i in range(randint(minPopulation, maxPopulation)):
    (y, x) = randint(0, boardSize - 1), randint(0, boardSize - 1)
    board[y][x] = 'X'

# DON'T THINK AN UPDATE IS REQUIRED
# initialise the count of generations and execute the main loop   
generations = 0
history = []

while generations < maxGenerations:
    print('\n'.join([''.join(x) for x in board]) + '\n')
    board, oldBoard = newCycle(board)
    if board == oldBoard:
        print('Static')
        break
    history.append(oldBoard)
    if checkOscillation(history, board) == 0:
        print('Oscillator reached')
        break
    sleep(0.1) # enter the time taken for each generation here
    generations += 1
