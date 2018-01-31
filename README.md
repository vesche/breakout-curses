# breakout-curses

This is a WIP primitive [breakout](https://en.wikipedia.org/wiki/Breakout_(video_game)) clone in Python that I'm making to learn more about curses.

## Fixing the "paddle stutter"
On most terminals the keyboard auto repeat rate is going to be too high and will making playing the game difficult. To see what your current settings are run `xset -q` and look for the values `auto repeat delay` and `repeat rate`.

I recommend you adjust these like so for playing: `xset -r 250 25`

## todo
* increase paddle speed
* collisions on sides of blocks
* fix weird counterspin paddle issues
