#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# breakout
# https://github.com/vesche
#

import curses
import board
import sys
import time

# 20x60 grid
HEIGHT = 19
WIDTH  = 59

# blocks - 1x6
BLOCK_SIZE = 6


def game(stdscr):
    # init game
    win = curses.newwin(HEIGHT, WIDTH, 0, 0)

    # init colors
    curses.start_color()
    curses.use_default_colors()
    for i in range(curses.COLORS):
        curses.init_pair(i+1, i, -1)

    # init vars
    running = True
    paddle_x = 27
    ball_x, ball_y = 32, 18
    ball_velocity = 0

    # init board
    blocks = board.checker('pink', 'tan')

    while running:
        # draw board
        for i in range(len(blocks)):
            color = blocks[i]
            stdscr.addstr(i/10, i%10*6, ' '*6, curses.color_pair(color) | curses.A_REVERSE)
        # draw paddle
        for i in range(11):
            stdscr.addstr(19, i+paddle_x, ' ', curses.color_pair(0) | curses.A_REVERSE)
        # draw ball
        stdscr.addstr(ball_y, ball_x, '*', curses.color_pair(4) |  curses.A_BOLD)

        # handle input
        c = stdscr.getch()
        if c == curses.KEY_RIGHT:
            if paddle_x < 49:
                paddle_x += 1
                # if ball has not launched yet
                if not ball_velocity:
                    ball_x += 1
            # ball spin
            spin = "left"
        elif c == curses.KEY_LEFT:
            if paddle_x > 0:
                paddle_x -= 1
                # if ball has not launched yet
                if not ball_velocity:
                    ball_x -= 1
            # ball spin
            spin = "right"
        elif c == curses.KEY_UP:
            ball_velocity = 1 # ball shit here
        elif c == ord('q'):
            running = False #sys.exit ?

        # collision walls
        # top wall

        # bounce off top and bottom
        if ball_y == 0:
            ball_velocity = 1
        if ball_y == 19:
            ball_velocity = -1

        

        # move ball up and down
        if ball_velocity:
            ball_y += ball_velocity


        # do things with ball

        # check win condition?
        # if tiles == wtiles: break

        # curses.napms(2000)
        # clear and refresh screen
        stdscr.refresh()

        # 60 FPS
        time.sleep(.0333)
        stdscr.clear()


def main():
    # init curses
    stdscr = curses.initscr()
    stdscr.nodelay(1)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(1)

    # gameplay loop
    game(stdscr)

    # teardown curses
    stdscr.keypad(0)
    curses.curs_set(1)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    main()
