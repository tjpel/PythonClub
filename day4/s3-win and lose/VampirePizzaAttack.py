"""
This final step adds ways to win and lose by adding a timer and a bad reviews system
    
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
WIDTH = 100
HEIGHT = 100
TILE_COLOR = WHITE


STARTING_BUCKS = 15
BUCK_RATE = 120
STARTING_BUCK_BOOSTER = 1

#define speeds
REG_SPEED = 2
SLOW_SPEED = 1


#Other
SPAWN_RATE = 360
FRAME_RATE = 60
ROWS = 6
COLUMNS = 11

#********************************************************
#win / lose
MAX_BAD_REVIEWS = 3
WIN_TIME = FRAME_RATE * 60 * 3 #3minutes
#**********************************************************

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
        #*****************************************************************
        self.rect = self.image.get_rect(center = (1100, y))
        #*******************************************************************
        #place the pizza in a rectange to the outside of the right side of the screen
        self.health = 100

    def update(self, game_window, counters):
        #Erase the last sprite image
        game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
        #Move the sprites
        self.rect.x -= self.speed
        #game_window.blit(self.image, (self.rect.x, self.rect.y))
        if self.health <= 0 or self.rect.x <= 100:
            self.kill()
            #******************************************************************************
            #if the pizza touches the delivery box, then we get a bad review
            if self.rect.x <= 100:
                counters.bad_reviews += 1
            #******************************************************************************
        else:
            game_window.blit(self.image, (self.rect.x, self.rect.y))
        
    


    def attack(self, tile):
        if tile.trap == SLOW:
            self.speed = SLOW_SPEED
        elif tile.trap == DAMAGE:
            self.health -= 1



#Background tiles class
class BackgroundTile(sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.trap = None
        self.rect = rect

#A subclass of Background tile where the player can set traps
class PlayTile(BackgroundTile):
    def set_trap(self, trap, counters):
        if bool(trap) and not bool(self.trap):
            counters.pizza_bucks -= trap.cost
            self.trap = trap
            if trap == EARN:
                counters.buck_booster += 1
        return None

    def draw_trap(self, game_window, trap_applicator):
        if bool(self.trap):
            game_window.blit(self.trap.trap_img, (self.rect.x, self.rect.y))

#A subclass of Background tile where the player can push buttons
class ButtonTile(BackgroundTile):
    def set_trap(self, trap, counters):
        if counters.pizza_bucks >= self.trap.cost:
            return self.trap
        else:
            return None

    def draw_trap(self, game_window, trap_applicator):
        if bool(trap_applicator.selected):
            if trap_applicator.selected == self.trap:
                draw.rect(game_window, (238, 190, 47), (self.rect.x, self.rect.y,
                WIDTH, HEIGHT), 5)

#A subclass of Background tile where the whole point is to do nothing
class InactiveTile(BackgroundTile):
    def set_trap(self, trap, counters):
        return None
    
    def draw_trap(self, game_window, trap_applicator):
        pass



class Counters(object):
    #Set up __init__ method with 4 arguements
    #*******************************************************REPLACE*************************
    #def __init__(self, pizza_bucks, buck_rate, buck_booster):
    def __init__(self, pizza_bucks, buck_rate, buck_booster, timer):
    #***************************************************************************************
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
        #***********************************ADD***********************************************
        self.timer = timer
        self.timer_rect = None
        self.bad_reviews = 0
        self.bad_rev_rect = None
        #*************************************************************************************

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

    #***************************************************************************************
    #Draw the player's bad reviews on to the screen
    def draw_bad_reviews(self, game_window):
        #test if there is a new number of bad reviews and erase the old # if there is
        if bool(self.bad_rev_rect):
            game_window.blit(BACKGROUND, (self.bad_rev_rect.x, self.bad_rev_rect.y), self.bad_rev_rect)
            
        #tell the program the font and color to use in the display
        bad_rev_surf = self.display_font.render(str(self.bad_reviews), True, WHITE)

        #set up a rect so that we can interact with the number
        self.bad_rev_rect = bad_rev_surf.get_rect()

        #put the display in the 2nd-to-last column and bottom row
        self.bad_rev_rect.x = WINDOW_WIDTH - 150
        self.bad_rev_rect.y = WINDOW_HEIGHT - 50

        #display the number to the screen
        game_window.blit(bad_rev_surf, self.bad_rev_rect)

    def draw_timer(self, game_window):
        if bool(self.timer_rect):
            game_window.blit(BACKGROUND, (self.timer_rect.x, self.timer_rect.y), self.timer_rect)
        timer_surf = self.display_font.render(str(WIN_TIME - self.loopCount // FRAME_RATE), True, WHITE)
        self.timer_rect = timer_surf.get_rect()
        self.timer_rect.x = WINDOW_WIDTH - 250
        self.timer_rect.y = WINDOW_HEIGHT - 50
        game_window.blit(timer_surf, self.timer_rect)

#****************************************************************************************************************

    def update(self, game_window):
        self.loopCount += 1
        self.increment_bucks()
        self.draw_bucks(game_window)
        #********************************************************************
        self.draw_bad_reviews(game_window)
        self.draw_timer(game_window)

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

#-------------------------------------------------
#Create class instances and groups

#Create a group for all the VampireSprites
all_vampires = sprite.Group()

#create a group for all the counters
#*******************************************************ADD TIMER ARGUMENT
counters = Counters(STARTING_BUCKS, BUCK_RATE, STARTING_BUCK_BOOSTER, WIN_TIME/60)

#initialize traps
SLOW = Trap('SLOW', 5, GARLIC)
DAMAGE = Trap('DAMAGE', 3, CUTTER)
EARN = Trap('EARN', 7, PEPPERONI)

trap_applicator = TrapApplicator()
#-------------------------------------------------
#Initialize and draw background grid
tileGrid = []
for row in range(ROWS):
    #create an empty list to put the new row in
    rowOfTiles = [] 
    #add the new list to the tile grid
    #tileGrid.append(rowOfTiles) 
    for column in range(COLUMNS):
        #create an invisible rectangle for each background tile sprite
        tileRect = Rect(WIDTH*column, HEIGHT*row, WIDTH, HEIGHT)

        if column <= 1:
            new_tile = InactiveTile(tileRect)
        else:
            if row == 5:
                if 2 <= column <= 4:
                    new_tile = ButtonTile(tileRect)
                    new_tile.trap = [SLOW, DAMAGE, EARN][column-2]
                else:
                    new_tile = InactiveTile(tileRect)
            else:
                new_tile = PlayTile(tileRect)
        rowOfTiles.append(new_tile)
        if row == 5 and 2 <= column <= 4:
            BACKGROUND.blit(new_tile.trap.trap_img, (new_tile.rect.x, new_tile.rect.y))
        elif column != 0 and row != 5:
            if column != 1:
                draw.rect(BACKGROUND, TILE_COLOR, (WIDTH*column, HEIGHT*row, WIDTH, HEIGHT), 1)

    tileGrid.append(rowOfTiles)


#display background
GAME_WINDOW.blit(BACKGROUND, (0,0))

#------------------------MAIN GAME LOOP----------------
#Start
game_running = True
#******************************************************************************************
program_running = True
#**************************************************************************

#Game loop
while game_running:

    #checking for events
    for event in pg.event.get():

        #Exit loop on quit
        if event.type == QUIT:
            game_running = False
            #***************************************************************************
            program_running = False
            #***************************************************************************
        #wait for the mouse button to me clicked and run this when clicked
        elif event.type == MOUSEBUTTONDOWN:
            #get the (x,y) coordinate where the mouse was clicked
            coordinates = mouse.get_pos()
            x = coordinates[0]
            y = coordinates[1]
            #find the background tile the click happened on and change effect to true
            tile_y = y // 100
            tile_x = x // 100

            trap_applicator.select_tile(tileGrid[tile_y][tile_x], counters)

        #spawn vampire pizza sprites
        if randint(1, SPAWN_RATE) == 1:
            VampireSprite()

        #draw the traps onto the grid
        for tileRow in tileGrid:
            for tile in tileRow:
                tile.draw_trap(GAME_WINDOW, trap_applicator)

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
            if bool(leftTile):
                vampire.attack(leftTile)

            
            #Test if the right side of the vamp is touching a tile and if that tile has been clicked
            if bool(rightTile):
                #check if the left and right sides of the vamp are touching diff tiles
                if rightTile != leftTile:
                    #if both are true, set the speed to 1
                    vampire.attack(rightTile)

            #delete the vamp sprite as it leaves the screen
            if vampire.rect.x <= 0:
                vampire.kill()

        #***************************************************************************************
        if counters.bad_reviews >= MAX_BAD_REVIEWS:
            game_running = False
        
        if counters.loopCount > WIN_TIME:
            game_running = False
        #**************************************************************************************

        #update display
        for vampire in all_vampires: #for each vampire in all_vampires
            vampire.update(GAME_WINDOW, counters)

        counters.update(GAME_WINDOW)
        display.update()

        clock.tick(FRAME_RATE)

#******************************************************************************************
#close game loop
end_font = font.Font('gameassets\\pizza_font.ttf', 50)
#test if either the win or lose conditoned happened
if program_running:
    if counters.bad_reviews >= MAX_BAD_REVIEWS:
        end_surf = end_font.render("Game Over", True, WHITE)
    else:
        end_surf = end_font.render("You Win!", True, WHITE)

GAME_WINDOW.blit(end_surf, (350, 200))
display.update()

#clean up
pg.quit()