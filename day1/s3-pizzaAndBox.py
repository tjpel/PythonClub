"""
Info for senseis:

syntax for drawing a circle and a rectangle
#draw.circle(WINDOW_OBJ, RGB_VAL, COORDS, radius, borderthickness)
#draw.rect(WINDOW_OBJ, RGB_VAL, (COORDS, SIZE), borderthickness)
NOTE: setting borderthickness to 0 will fill the shape
example calls:
draw.circle(GAME_WINDOW, (255, 0, 0), (925, 425), 25, 0)
draw.rect(GAME_WINDOW, (160, 82, 45), (895, 395, 110, 110), 5)

There are two slashes in the storage location for variables as /v is an escape operator in strings.
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

#NOTE: THIS IS NEW DOWN TO THE STARS ****************************
#import vampire pizza
pizza_img = image.load('PythonClub\gameassets\\vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (100, 100))
GAME_WINDOW.blit(VAMPIRE_PIZZA, (900, 400)) #.blit adds the object to the screen .blit(surface, (location tuple))

#add a giant pepperoni
draw.circle(GAME_WINDOW, (255, 0, 0), (925, 425), 25, 0)

#pizza box
draw.rect(GAME_WINDOW, (160, 82, 45), (895, 395, 110, 110), 5)
#pizza lid
draw.rect(GAME_WINDOW, (160, 82, 45), (895, 295, 110, 110), 0)
#*******************************************************************

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