"""
This step is for making the actual collisions happen.
Define the new speeds at the top first
Single point insertions on line 91, 198, 205
"""

import pygame as pg
from pygame import *
import time as t
from random import randint

#Start pygame
pg.init()

#set up a clock
clock = time.Clock()

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

#***********************
#define speeds
REG_SPEED = 2
SLOW_SPEED = 1
#***********************

#Other
SPAWN_RATE = 180
FRAME_RATE = 60

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
#Create class system

#Create a subclass of Sprite called VampireSprite
class VampireSprite(sprite.Sprite):

    #Define the VampireSprite set-up method
    def __init__(self):
        #Use everything from sprite to make sprite
        super().__init__()
        #Set the speed
        self.speed = REG_SPEED #*
        #Randomly select the lane the monster will be in from 0 and 4
        self.lane = randint(0, 4)
        #Add all vampire pizza sprites to a group so you can control them all together
        all_vampires.add(self)
        #Use the VAMPIRE_PIZZA image for the sprite
        self.image = VAMPIRE_PIZZA.copy()
        #Set the sprites y value to be the middle of the lane that was randomly selected
        y = 50 + (self.lane * 100)
        #place the pizza in a rectange to the outside of the right side of the screen
        self.rect = self.image.get_rect(center = (1100, y))

    def update(self, game_window):
        #Erase the last sprite image
        game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        #Move the sprites
        self.rect.x -= self.speed
        game_window.blit(self.image, (self.rect.x, self.rect.y))

#Background tiles class
class BackgroundTile(sprite.Sprite):

    def __init__(self, rect):
        super().__init__()
        self.effect = False
        self.rect = rect
#-------------------------------------------------
#Create class instances and groups

#Create a group for all the VampireSprites
all_vampires = sprite.Group()
#-------------------------------------------------
#Initialize and draw background grid
tileGrid = []
for row in range(ROWS):
    #create an empty list to put the new row in
    rowOfTiles = [] 
    #add the new list to the tile grid
    tileGrid.append(rowOfTiles) 
    for column in range(COLUMNS):
        #create an invisible rectangle for each background tile sprite
        tileRect = Rect(WIDTH*column, HEIGHT*row, WIDTH, HEIGHT)
        #for each column and each row, create a new background tile sprite
        newTile = BackgroundTile(tileRect)
        #add the new tile to the correct list
        rowOfTiles.append(newTile)
        draw.rect(BACKGROUND, TILE_COLOR, (WIDTH*column, HEIGHT*row, WIDTH, HEIGHT), 1)


#display background
GAME_WINDOW.blit(BACKGROUND, (0,0))

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
        #wait for the mouse button to me clicked and run this when clicked
        elif event.type == MOUSEBUTTONDOWN:
            #get the (x,y) coordinate where the mouse was clicked
            coordinates = mouse.get_pos()
            x = coordinates[0]
            y = coordinates[1]
            #find the background tile the click happened on and change effect to true
            tile_y = y // 100
            tile_x = x // 100
            tileGrid[tile_y][tile_x].effect = True #hold up, what does this do? why y,x?

        #spawn vampire pizza sprites
        if randint(1, SPAWN_RATE) == 1:
            VampireSprite()

        #*******************************************
        #-------------------------------------------
        #Set up collision detection
        #for each vampire
        for vampire in all_vampires:
            #store the row that the vampire is in
            tileRow = tileGrid[vampire.rect.y // 100]
            #find the left and right sides
            vampLeftSide = vampire.rect.x // 100
            vampRightSide = (vampire.rect.x + vampire.rect.width) // 100

            #if the vamp is on the grid, find which column it's in
            if 0 <= vampLeftSide <= 10:
                leftTile = tileRow[vampLeftSide]
            #set it to nothing if the vamp is not on the grid
            else:
                leftTile = None

            #same as left
            if 0 <= vampRightSide <= 10:
                rightTile = tileRow[vampRightSide]
            else:
                rightTile = None

            #Test if the left side of the vamp is touching a tile where there is a trap
            #If it is, set the speed to 1
            if bool(leftTile) and leftTile.effect:
                vampire.speed = SLOW_SPEED #*
            
            #Test if the right side of the vamp is touching a tile and if that tile has been clicked
            if bool(rightTile) and rightTile.effect:
                #check if the left and right sides of the vamp are touching diff tiles
                if rightTile != leftTile:
                    #if both are true, set the speed to 1
                    vampire.speed = SLOW_SPEED #*

            #delete the vamp sprite as it leaves the screen
            if vampire.rect.x <= 0:
                vampire.kill()
        #*******************************************************************************

        #update display
        for vampire in all_vampires: #for each vampire in all_vampires
            vampire.update(GAME_WINDOW)

        display.update()

        clock.tick(FRAME_RATE)

#clean up
pg.quit()