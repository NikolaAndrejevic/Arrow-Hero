import pygame, sys
from pygame.locals import *
import os
os.environ['SDL_VIDEODRIVER']='windib'
pygame.init()

FPS = 25 # frames per second setting

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ARROWHOLDER = pygame.image.load('Arrow Holder.png')
RIGHT= pygame.image.load('Right Arrow.png')
UP= pygame.image.load('Up Arrow.png')
DOWN= pygame.image.load('Down Arrow.png')
LEFT = pygame.image.load('Left Arrow.png')
A = "Awesome"
B = "Great"
C = "OK"
F = "Missed"
N = "Not Played yet"
ARROWHOLDERX = 400
ARROWHOLDERY = 520

RIGHTARROWX = 587
UPARROWX = 524
DOWNARROWX = 461
LEFTARROWX = 397
SPEED = 4
STARTINGPOSITION = -80.00
ARROWLIST = []
ARROWCURRENTPOSLIST = []
arrowHitResult = []
for item in ARROWLIST:
    ARROWCURRENTPOSLIST.append(-500.00)
    arrowHitResult.append(N)
currentArrow = 0
time = 0
next_arrow_to_press = 0
score = 0
class arrow:
    def __init__(self, pic=None, ypos=None):
        self.pic = pic
        self.ypos = ypos

def check_if_arrow_hit(next_arrow_to_press,score,arrowdirection):
    if ARROWHOLDERY - 15 < (ARROWCURRENTPOSLIST[next_arrow_to_press]) and  ARROWHOLDERY + 15 > (ARROWCURRENTPOSLIST[next_arrow_to_press]) and ARROWLIST[next_arrow_to_press][0] == arrowdirection:            
        score += 300
        arrowHitResult[next_arrow_to_press] = A
        if next_arrow_to_press < len(arrowHitResult) -1:
            next_arrow_to_press += 1
        
    elif ARROWHOLDERY - 25 < (ARROWCURRENTPOSLIST[next_arrow_to_press]) and  ARROWHOLDERY + 25> (ARROWCURRENTPOSLIST[next_arrow_to_press]) and ARROWLIST[next_arrow_to_press][0] == arrowdirection:
        score += 100
        arrowHitResult[next_arrow_to_press] = B
        if next_arrow_to_press < len(arrowHitResult) -1:
            next_arrow_to_press += 1
    elif ARROWHOLDERY - 40 < (ARROWCURRENTPOSLIST[next_arrow_to_press]) and  ARROWHOLDERY + 40> (ARROWCURRENTPOSLIST[next_arrow_to_press]) and ARROWLIST[next_arrow_to_press][0] == arrowdirection:
        score += 50
        arrowHitResult[next_arrow_to_press] = C
        if next_arrow_to_press < len(arrowHitResult) -1:
            next_arrow_to_press += 1
    return next_arrow_to_press, score

# set up the window
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Arrow Hero')

##pygame.mixer.music.load()
##pygame.mixer.music.play(0)
pygame.mixer.init()
song = raw_input("Song Name:")
pygame.mixer.music.load(song)



while True: # the main game loop
    pygame.mixer.music.play(0,time)
 
    DISPLAYSURF.fill(WHITE)
    




    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == KEYDOWN:
            time1 =  time

        if event.type == KEYUP:
            if time1 < time - .20:
                if event.key == K_UP:
                    ARROWLIST.append(['UP',round(time1,2),round(time,2)])

                if event.key == K_DOWN:
                   ARROWLIST.append(['DOWN',round(time1,2),round(time,2)])

                if event.key == K_LEFT:
                   ARROWLIST.append(['LEFT',round(time1,2),round(time,2)])

                if event.key == K_RIGHT:
                    ARROWLIST.append(['RIGHT',round(time1,2),round(time,2)])
                    
                if event.key == K_TAB:
                    print ARROWLIST 
            else:
                if event.key == K_UP:
                    ARROWLIST.append(['UP',round(time1,2)])

                if event.key == K_DOWN:
                   ARROWLIST.append(['DOWN',round(time1,2)])

                if event.key == K_LEFT:
                   ARROWLIST.append(['LEFT',round(time1,2)])

                if event.key == K_RIGHT:
                    ARROWLIST.append(['RIGHT',round(time1,2)])
                    
                if event.key == K_TAB:
                    print ARROWLIST 
            

    pygame.display.update()
    fpsClock.tick(FPS)
    time += .04
    
    

