"""
This step adds different trap types, including the images for them, 2 classes for making and applying them,
and changes lines to incorperate this new system.
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


STARTING_BUCKS = 15
BUCK_RATE = 60 #halfed for frame rate halved
STARTING_BUCK_BOOSTER = 1

#define speeds
REG_SPEED = 2
SLOW_SPEED = 1

#Other
SPAWN_RATE = 180
FRAME_RATE = 30 #halfed

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

#*************************************************************************************
#import garlic trap
garlic_img = image.load('gameassets\\garlic.png')
garlic_surf = Surface.convert_alpha(garlic_img)
GARLIC = transform.scale(garlic_surf, (WIDTH, HEIGHT))

#set up pizza cutter
cutter_img = image.load('gameassets\\pizzacutter.png')
cutter_surf = Surface.convert_alpha(cutter_img)
CUTTER = transform.scale(cutter_surf, (WIDTH, HEIGHT))

#set up pepperoni img
pepp_img = image.load('gameassets\\pepperoni.png')
pepp_surf = Surface.convert_alpha(pepp_img)
PEPPERONI = transform.scale(pepp_surf, (WIDTH, HEIGHT))
#**************************************************************************************
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

class Counters(object):
    #Set up __init__ method with 4 arguements
    def __init__(self, pizza_bucks, buck_rate, buck_booster):
        #start the game loop counter at 0
        self.loopCount = 0
        #set up the font of the counter
        self.display_font = font.Font('gameassets\pizza_font.ttf', 25)
        #define pizza bucks attribute using the pizza bucks arguement
        self.pizza_bucks = pizza_bucks
        self.buck_rate = buck_rate
        self.buck_booster = buck_booster
        #do we want a rectangle around the counters?
        self.bucks_rect = None

    def increment_bucks(self):
        if self.loopCount % self.buck_rate == 0:
            self.pizza_bucks += self.buck_booster

    def draw_bucks(self, game_window):
        #erase the last number from the game window
        if bool(self.bucks_rect):
            game_window.blit(BACKGROUND, (self.bucks_rect.x, self.bucks_rect.y), self.bucks_rect)

        bucks_surf = self.display_font.render(str(self.pizza_bucks), True, WHITE)
        
        #create a rect for bucks_surf
        self.bucks_rect = bucks_surf.get_rect()

        #place the counter in the middle of the bottom-right corner
        self.bucks_rect.x = WINDOW_WIDTH - 50
        self.bucks_rect.y = WINDOW_HEIGHT - 50

        #display the new total
        game_window.blit(bucks_surf, self.bucks_rect)

    def update(self, game_window):
        self.loopCount += 1
        self.increment_bucks()
        self.draw_bucks(game_window)

#***************************************************************************
#Traps Class
class Trap(object):
    def __init__(self, trap_kind, cost, trap_img):
        self.trap_kind = trap_kind
        self.cost = cost
        self.trap_img = trap_img

#Trap applicator class
class TrapApplicator(object):
    def __init__(self):
        self.selected = None

    def select_trap(self, trap):
        if trap.cost <= counters.pizza_bucks:
            self.selected = trap

    def select_tile(self, tile, counters):
        self.selected = tile.set_trap(self.selected, counters)
#****************************************************************************

#-------------------------------------------------
#Create class instances and groups

#Create a group for all the VampireSprites
all_vampires = sprite.Group()

#create a group for all the counters
counters = Counters(STARTING_BUCKS, BUCK_RATE, STARTING_BUCK_BOOSTER)

#***************************************************************************
#initialize traps
SLOW = Trap('SLOW', 5, GARLIC)
DAMAGE = Trap('DAMAGE', 3, CUTTER)
EARN = Trap('EARN', 7, PEPPERONI)

trap_applicator = TrapApplicator()
#****************************************************************************)
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
            #**************************************************************************************
            #DELETE BELOW
            #tileGrid[tile_y][tile_x].effect = True #hold up, what does this do? why y,x?
            #ADD
            trap_applicator.select_tile(tileGrid[tile_y][tile_x], counters)
            #*************************************************************************************

        #spawn vampire pizza sprites
        if randint(1, SPAWN_RATE) == 1:
            VampireSprite()

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

        #update display
        for vampire in all_vampires: #for each vampire in all_vampires
            vampire.update(GAME_WINDOW)

        counters.update(GAME_WINDOW)
        display.update()

        clock.tick(FRAME_RATE)

#clean up
pg.quit()