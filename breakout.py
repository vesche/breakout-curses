#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# breakout using curses
# https://github.com/vesche
#

import curses
import time
import board

# consts
HEIGHT = 19 # 20x60 grid
WIDTH = 59
BLOCK_SIZE = 6 # 1x6 block
B_ROWS = 5 # 10 blocks in top 5 rows
B_COLS = 10
PADDLE_SIZE = 11
BLK = 17 # color code for black
DEBUG = True


def game(stdscr):
    # init colors
    curses.start_color()
    curses.use_default_colors()
    for i in range(curses.COLORS):
        curses.init_pair(i+1, i, -1)

    # init vars
    running = True
    launched = False
    paddle_x = 27
    ball_x, ball_y, ball_v = 32, 18, 0
    spin = None
    block_spin = None

    # init board
    blocks = board.checker("yellow", "blue")

    # gameplay loop
    while running:
        ##############
        # draw scene #
        ##############
        # draw board
        for i in range(len(blocks)):
            color = blocks[i]
            stdscr.addstr(i//B_COLS, i%B_COLS*BLOCK_SIZE, ' '*BLOCK_SIZE,
                curses.color_pair(color) | curses.A_REVERSE)

        # draw paddle
        for i in range(PADDLE_SIZE):
            stdscr.addstr(HEIGHT, i+paddle_x, ' ',
                curses.color_pair(0) | curses.A_REVERSE)

        # draw ball
        stdscr.addstr(ball_y, ball_x, '*',
            curses.color_pair(4) |  curses.A_BOLD)

        ################
        # handle input #
        ################
        # get key
        key = stdscr.getch()

        # move paddle right
        if key == curses.KEY_RIGHT:
            if paddle_x < 49:
                paddle_x += 1
                # ball not yet launched
                if not ball_v:
                    ball_x += 1
            # ball spin
            if ball_y == 18 and ball_v:
                spin = "left"

        # move paddle left
        elif key == curses.KEY_LEFT:
            if paddle_x > 0:
                paddle_x -= 1
                # ball not yet launched
                if not ball_v:
                    ball_x -= 1
            # ball spin
            if ball_y == 18 and ball_v:
                spin = "right"

        # move up (launch ball)
        elif key == curses.KEY_UP:
            ball_v = -1
            launched = True

        # quit game
        elif key == ord('q'):
            running = False

        ##############
        # game logic #
        ##############
        # ball top collision
        if ball_y == 0:
            ball_v = 1

        # ball/paddle collision
        if launched and ball_y == 18 and \
        (paddle_x <= ball_x < paddle_x+PADDLE_SIZE):
            ball_v = -1

        # ball brick collision
        if ball_y-1 < B_ROWS:
            # this is hacky (collision should have its own funcs)
            for i in range(1):
                # break block above
                if (blocks[B_COLS*(ball_y-1) + ball_x//BLOCK_SIZE] != BLK):
                    ball_v = 1
                    blocks[B_COLS*(ball_y-1) + ball_x//BLOCK_SIZE] = BLK
                    break
                # break block to side and get new spin
                try:
                    if spin == "right":
                        if (blocks[B_COLS*(ball_y) + (ball_x+1)//BLOCK_SIZE] != BLK):
                            blocks[B_COLS*(ball_y) + (ball_x+1)//BLOCK_SIZE] = BLK
                            spin = "left"
                    elif spin == "left":
                        if (blocks[B_COLS*(ball_y) + (ball_x-1)//BLOCK_SIZE] != BLK):
                            blocks[B_COLS*(ball_y) + (ball_x-1)//BLOCK_SIZE] = BLK
                            spin = "right"
                except: pass

        # ball misses paddle and passes outside of map
        if ball_y == 20:
            if DEBUG:
                # reset ball
                ball_x, ball_y, ball_v = paddle_x+5, 18, 0
                spin = None
                launched = False
            else:
                running = False

        # ball spin from paddle
        if spin == "left":
            ball_x -= 1
        elif spin == "right":
            ball_x += 1

        # ball spin wall collision
        if ball_x == 0:
            spin = "right"
        if ball_x == 59:
            spin = "left"

        # ball moving up and down
        if ball_v:
            ball_y += ball_v

        ###########
        # display #
        ###########
        # refresh, delay (24FPS), clear screen
        stdscr.refresh()
        time.sleep(1/24.0)
        stdscr.clear()


def main():
    # init curses
    stdscr = curses.initscr()
    stdscr.nodelay(1)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)

    # start game
    game(stdscr)

    # teardown curses
    stdscr.keypad(0)
    curses.curs_set(1)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    main()
