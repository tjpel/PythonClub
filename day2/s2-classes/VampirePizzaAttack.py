"""
This step introduces addition files to build a class system. From now on, the file we've worked
on will be called "VampirePizzaAttack.py", as it always should've been for the kids.
A new file named "MonsterFoods.py will be made.
This documentation will continue to be in this file.
"""

import pygame as pg
from pygame import *
import time as t

#Start pygame
pg.init()

#-----------------------------------------------
#define constants

#game window
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)

#color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#tile constants
ROWS = 6
COLUMNS = 11
WIDTH = 100
HEIGHT = 100
TILE_COLOR = WHITE

#------------------------------------------------
#load assets

#create window
GAME_WINDOW = display.set_mode(WINDOW_RES)
display.set_caption('Attack of the Vampire Pizzas!')

#import vampire pizza
pizza_img = image.load('gameassets\\vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (100, 100))
GAME_WINDOW.blit(VAMPIRE_PIZZA, (900, 400))

#add a giant pepperoni
draw.circle(GAME_WINDOW, (255, 0, 0), (925, 425), 25, 0)

#pizza box
draw.rect(GAME_WINDOW, (160, 82, 45), (895, 395, 110, 110), 5)
#pizza lid
draw.rect(GAME_WINDOW, (160, 82, 45), (895, 295, 110, 110), 0)

#makes a "loading screen"
display.update()
t.sleep(2)

#load and transform background
background_img = image.load('gameassets\\restaurant.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, WINDOW_RES)

#-------------------------------------------------
#Initialize and draw background grid
for row in range(ROWS):
    for column in range(COLUMNS):
        draw.rect(BACKGROUND, TILE_COLOR, (WIDTH*column, HEIGHT*row, WIDTH, HEIGHT), 1)


#display background and vampire pizza
GAME_WINDOW.blit(BACKGROUND, (0,0))
GAME_WINDOW.blit(VAMPIRE_PIZZA, (900, 400))

#------------------------MAIN GAME LOOP----------------
#Start
game_running = True

#Game loop
while(game_running):

    #checking for events
    for event in pg.event.get():

        #Exit loop on quit
        if event.type == QUIT:
            game_running = False

        #update display
        display.update()

#clean up
pg.quit()