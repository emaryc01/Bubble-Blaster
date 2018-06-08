#Bubble Blaster Game #

## import from libraries##
from tkinter import *
from random import randint
import random
from time import sleep, time
from math import sqrt
import winsound
import ctypes

###functions###

#This function moves the ship when the arrow keys are pressed
def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -SHIP_SPD)
        c.move(ship_id2, 0, -SHIP_SPD)
    elif event.keysym == 'Down':
        c.move(ship_id, 0, SHIP_SPD)
        c.move(ship_id2, 0, SHIP_SPD)
    elif event.keysym == 'Left':
        c.move(ship_id, -SHIP_SPD, 0)
        c.move(ship_id2,-SHIP_SPD, 0)
    elif event.keysym == 'Right':
        c.move(ship_id, SHIP_SPD, 0)
        c.move(ship_id2, SHIP_SPD, 0)

#This function creates individual bubbles and assigns them a speed and a size at random
def create_bubble():
    x = WIDTH + GAP
    y = randint(0,HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    colours = ['white','red','green','blue','red','green','blue','red','green','blue','red','blue','red','blue','red','blue']
    colour = random.choice(colours)
    id1 = c.create_oval(x-r, y-r, x+r, y+r, outline = colour)
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPD))
    bub_colour.append(colour)

#This function makes the bubbles move from right to left
def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)

#This function returns the position of a shape. It's used later by the distance function
def get_coords(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x,y

# This function deletes a bubble, it's used later by the collision function
def del_bubble(i):
    del bub_r[i]
    del bub_speed[i]
    c.delete(bub_id[i])
    del bub_id[i]


# This function removes any bubbles which have moved off the screen
def clean_up_bubs():
    for i in range(len(bub_id)-1, -1, -1):
        x,y = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)

# This function ccompares the distance between the ship and the bubbles.  It's used later by the collision function
def distance(id1, id2):
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2-x1)**2+(y2-y1)**2)

# This function controls collision of ship and bubble (checks distance, adds points and deletes bubble)
def collision():
    points = 0
    for bub in range(len(bub_id)-1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]):
            
            if bub_colour[bub] == 'white':
               points +=((bub_r[bub]+bub_speed[bub]+100))
            elif bub_colour[bub] == 'green':
               points -=100  
            else:
               points +=(bub_r[bub]+bub_speed[bub])
            del_bubble(bub)
    return points

#These functions display score and time left
def show_score(score):
    c.itemconfig(score_text, text = str(score))

def show_time(time_left):
    c.itemconfig(time_text, text = str(time_left))

####  create variables and set up stage####

#set up background
HEIGHT = 500
WIDTH = 800
root = Tk()
root.title = ('Bubble Blaster')
frame = Frame(root, bd=5, relief = SUNKEN)
frame.pack()
c = Canvas(frame, width = WIDTH, height = HEIGHT, bg='darkblue')
c.pack()

#create ship and allow movement
ship_id = c.create_polygon(5, 5, 5 ,25 ,30 ,15 ,fill='red')
ship_id2= c.create_oval(0, 0, 30 ,30 , outline = 'red')
SHIP_R = 15
MID_X = WIDTH/2
MID_Y = HEIGHT/2
c.move(ship_id, MID_X, MID_Y)
c.move(ship_id2, MID_X, MID_Y)
SHIP_SPD = 10
c.bind_all('<Key>', move_ship)

#bubble value lists and ranges
bub_id = list()
bub_r = list()
bub_speed = list()
bub_colour = list()
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPD = 10
GAP = 100
BUB_CHANCE = 10

#set up progress board and variables
c.create_text(50, 30, text = 'TIME', fill = 'white')
c.create_text(150, 30, text = 'SCORE', fill = 'white')
time_text = c.create_text(50, 50, fill = 'white')
score_text = c.create_text(150, 50, fill = 'white')
BUB_CHANCE = 10
TIME_LIMIT = 30
BONUS_SCORE = 1000
score = 0
bonus = 0
end = time()+TIME_LIMIT


#####MAIN GAME LOOP#####

winsound.PlaySound("Bubbleshoot Theme Music.wav",  winsound.SND_LOOP + winsound.SND_ASYNC)

#loop until no time left in game
while time()<end:
    #only create a bubble if random number generated is 1
    if randint(1, BUB_CHANCE) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    score+=collision()
    #Add bonus time if score is high enough
    if(int(score/BONUS_SCORE))>bonus:
        bonus+=1
        end +=TIME_LIMIT
    show_score(score)
    show_time(int(end-time()))
    root.update()
    sleep(0.01)

###End screen and stop sound
winsound.PlaySound(None, winsound.SND_FILENAME)
c.create_text(MID_X, MID_Y, text = 'GAME OVER', fill = 'white', font = ('Helvetica', 30))
c.create_text(MID_X, MID_Y + 30, text = 'Score: ' + str(score), fill = 'white')
c.create_text(MID_X, MID_Y + 45, text = 'Bonus Time: ' + str(bonus*TIME_LIMIT), fill = 'white')

#changes to original code
#1.Created bubble of random colours, white = bonus points, green = negative points
#2.Play background sound on loop
#3.Used root instead of window (to overcome error message when closing window)
#4.Improved structure of code




        

