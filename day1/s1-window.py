"""
Info for senseis:

For import ___ as ____ statements, the as _____ is optional and can be called whatever you want.
In this step, the window is supposed to only appear for a moment then go away.
"""


import pygame as pg
from pygame import *

#Start pygame
pg.init()

#-----------------------------------------------
#define constants

#game window
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)

#------------------------------------------------
#load assets

#create window
GAME_WINDOW = display.set_mode(WINDOW_RES)
display.set_caption('Attack of the Vampire Pizzas!')