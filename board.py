# -*- coding: utf-8 -*-

from random import randint
from breakout import B_ROWS, B_COLS

COLORS = ['white', 'grey', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan']


def checker(color_a, color_b):
    board = []
    code_a = COLORS.index(color_a)
    code_b = COLORS.index(color_b)
    for i in range(B_ROWS):
        if i % 2:
            board += [code_a, code_b]*(B_COLS//2)
        else:
            board += [code_a, code_b][::-1]*(B_COLS//2)
    return board


def standard():
    board = []
    for i in range(2, B_ROWS+2):
        board += [i]*B_COLS
    return board


def random():
    board = []
    for i in range(B_ROWS):
        board += [randint(0, 7) for _ in range(10)]
    return board