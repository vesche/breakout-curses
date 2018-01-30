#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# breakout using curses.
# https://github.com/vesche
#

import curses
import time
import board

# consts
HEIGHT = 19 # 20x60 grid
WIDTH = 59
BLOCK_SIZE = 6 # 1x6 block
PADDLE_SIZE = 11
DEBUG = True


def game(stdscr):
    # init colors
    curses.start_color()
    curses.use_default_colors()
    for i in range(curses.COLORS):
        curses.init_pair(i+1, i, -1)

    # init vars
    running = True
    paddle_x = 27
    ball_x, ball_y = 32, 18
    ball_vy, ball_xy = 0, 0
    spin = None

    # init board
    blocks = board.checker("white", "red")

    # gameplay loop
    while running:
        # draw board
        for i in range(len(blocks)):
            color = blocks[i]
            stdscr.addstr(i//10, i%10*6, ' '*6, curses.color_pair(color) | curses.A_REVERSE)
        # draw paddle
        for i in range(PADDLE_SIZE):
            stdscr.addstr(19, i+paddle_x, ' ', curses.color_pair(0) | curses.A_REVERSE)
        # draw ball
        stdscr.addstr(ball_y, ball_x, '*', curses.color_pair(4) |  curses.A_BOLD)

        # handle input
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:
            if paddle_x < 49:
                paddle_x += 1
                # ball has not launched yet
                if not ball_vy:
                    ball_x += 1
            # ball spin
            if ball_y == 18:
                spin = "left"
        elif key == curses.KEY_LEFT:
            if paddle_x > 0:
                paddle_x -= 1
                # ball has not launched yet
                if not ball_vy:
                    ball_x -= 1
            # ball spin
            if ball_y == 18:
                spin = "right"
        elif key == curses.KEY_UP:
            ball_vy = 1
        elif key == ord('q'):
            running = False

        # ball top collision (tmp)
        if ball_y == 0:
            ball_vy = 1

        # ball/paddle collision 
        if ball_y == 18 and (paddle_x <= ball_x < paddle_x+PADDLE_SIZE):
            ball_vy = -1

        # ball misses paddle
        if ball_y == 19:
            if DEBUG:
                # reset ball
                ball_vy = 0
                ball_x, ball_y = paddle_x+5, 18
                spin = None
            else:
                running = False

        # ball spin from paddle
        if spin == "left":
            ball_x -= 1
        elif spin == "right":
            ball_x += 1

        # ball left/right wall collision
        if ball_x == 0:
            spin = "right"
        if ball_x == 59:
            spin = "left"

        # ball moving up and down
        if ball_vy:
            ball_y += ball_vy

        # refresh, delay (30FPS), clear screen
        stdscr.refresh()
        time.sleep(1/30.0)
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
