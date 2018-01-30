
#
# blocks.py
#

from random import randint

COLORS = ['white', 'grey', 'red', 'green', 'yellow', 'orange', 'tan', 'pink']
ROWS = 5
COLS = 10

def checker(color_a, color_b):
    board = []
    code_a = COLORS.index(color_a)
    code_b = COLORS.index(color_b)
    for i in range(ROWS):
        if i % 2:
            board += [code_a, code_b]*(COLS//2)
        else:
            board += [code_a, code_b][::-1]*(COLS//2)
    return board

def standard():
    board = []
    for i in range(2, ROWS+2):
        board += [i]*COLS
    return board

def random():
    board = []
    for i in range(ROWS):
        board += [randint(0, 7) for _ in range(10)]
    return board
