#Nikola Andrejevic
#Arrow Hero

import pygame, sys
from pygame.locals import *
import os
import numpy
import pyganim
import easygui as eg
from ast import literal_eval
os.environ['SDL_VIDEODRIVER']='windib'
pygame.init()
pygame.mixer.init()
USERNAMELIST = []
HIGHSCORELIST = []
HIGHSCORETXT = []

def getHighScores(songNumber,score):
    
    ''' (interger,interger)-> list,list

        Takes the song number and score and figures out whether the player
        made it to the highscore list. If they did, the highscore list file
        is modified. USERNAMESLIST, the list of highest names and HIGHSCORELIST, the
        list of the highest scores is returned.
    '''

        
    f =  open("highscores.txt")
    for i in range(10*songNumber):
        line = f.readline()
        line = line.replace('"', '').strip()
        HIGHSCORETXT.append(line)        
    for i in range(5):
        line = f.readline()
        line = line.replace('"', '').strip()
        USERNAMELIST.append(line)
        HIGHSCORETXT.append(line)
    for i in range(5):
        line = f.readline()
        line = line.replace('"', '').strip()
        HIGHSCORELIST.append(int(line))
        HIGHSCORETXT.append(line)
    while line != "":
        line = f.readline()
        line = line.replace('"', '').strip()
        HIGHSCORETXT.append(line)
    HIGHSCORETXT.pop()


    if score > HIGHSCORELIST[4]:
        name = eg.enterbox(msg='Enter Your Name', title=' ', default='', strip=True)
        name = name[:10]
        HIGHSCORELIST.append(score)
        USERNAMELIST.append(name)
        for i in range(6):
            for j in range(5):
                if HIGHSCORELIST[j]<HIGHSCORELIST[j+1]:
                    HIGHSCORELIST[j],HIGHSCORELIST[j+1] = HIGHSCORELIST[j+1],HIGHSCORELIST[j]
                    USERNAMELIST[j],USERNAMELIST[j+1] = USERNAMELIST[j+1],USERNAMELIST[j]
        HIGHSCORELIST.pop()
        USERNAMELIST.pop()
        for i in range(10*songNumber,(10*songNumber)+5):
            HIGHSCORETXT[i] = USERNAMELIST[i-(10*songNumber)]
        for i in range((10*songNumber)+5,(10*songNumber)+10):
            HIGHSCORETXT[i] = HIGHSCORELIST[i-(10*songNumber+5)]

            
        g = open("highscores.txt", "w")
        for i in range(len(HIGHSCORETXT)):
            g.write(str(HIGHSCORETXT[i])+"\n")
        g.close()
        
    print USERNAMELIST,HIGHSCORELIST
    return USERNAMELIST,HIGHSCORELIST

def displayHighScores(USERNAMELIST,HIGHSCORELIST):
    ''' (list,list)-> 

        Takes the list of the best names and the list of the highest scores
        and displays them on the screen.
    '''
    for i in range(len(USERNAMELIST)):
        label = font3.render(str(i+1)+".  " + str(USERNAMELIST[i])+":", 1, (255,255,255))
        DISPLAYSURF.blit(label,(260,300+(30*i)))
        label = font3.render(str(HIGHSCORELIST[i]), 1, (255,255,255))
        DISPLAYSURF.blit(label,(500,300+(30*i)))
    label = font5.render("High Scores", 1, (255,255,255))
    DISPLAYSURF.blit(label,(215,180))   
    return
        
            

def countResults():
    '''()->list,string

        Calculates stats based on the list, arrowHitResult. The results are
        stored in the list,RESULTSACT, which is returned and an appropriate
        letter score is calculated and also returned.

    '''
    awesome = 0
    great = 0
    ok = 0
    missed = 0
    hit = 0
    streak = 0
    maxstreak = 0
    maxscore = (len(ARROWLIST)*300)
    for i in range(len(ARROWLIST)):
        if arrowHitResult[i] == "Awesome":
            awesome +=1
            hit +=1
            streak += 1
        if arrowHitResult[i] == "Great":
            great +=1
            hit +=1
            streak += 1
        if arrowHitResult[i] == "OK":
            ok +=1
            hit +=1
            streak += 1
        if arrowHitResult[i] == "Missed":
            missed +=1
            if streak > maxstreak:
                maxstreak = streak
            streak = 0
    percentage =float(hit)/(hit+missed)*100
    RESULTSACT = [awesome,great,ok,missed,maxstreak,str(round(percentage,2))+"%"]
    if score == maxscore:
        lettergrade = "SS"
    elif score > maxscore*.97:
        lettergrade = "S"
    elif score > maxscore * .90:
        lettergrade = "A"
    elif score > maxscore * .80:
        lettergrade = "B"
    elif score > maxscore * .65:
        lettergrade = "C"
    elif passingpoints > 0:
        lettergrade = "D"
    else:
        lettergrade = "F"
    return (RESULTSACT,lettergrade)

def displayResults(score,lettergrade):
    '''(int,string)->

        Takes the player's score, along with the calculated lettergrade
        and statistics stored in RESULTSACT and displays the information
        on the screen.
        

    '''
    
    for i in range(len(RESULTPAGELIST1)):
        label = font3.render(RESULTPAGELIST1[i], 1, (255,255,255))
        DISPLAYSURF.blit(label, (180,180+(40*i)))
    for i in range(len(RESULTPAGELIST2)):
        label = font3.render(RESULTPAGELIST2[i], 1, (255,255,255))
        DISPLAYSURF.blit(label, (450,180+(40*i)))
    for i in range(len(RESULTSACT)):
        label = font3.render(str(RESULTSACT[i]), 1, (255,255,255))
        DISPLAYSURF.blit(label,RESULTSCOOR[i])
    label = font.render(str(score), 1, (255,255,255))
    DISPLAYSURF.blit(label,(390,505))
    label = font.render("Score:", 1, (255,255,255))
    DISPLAYSURF.blit(label,(130,500))
    label = font4.render(lettergrade, 1,(255,0,0))
    DISPLAYSURF.blit(label,(320,280))
    return
          
def MakeHeldArrowList():
    '''()->

        Uses global list, ARROWLIST, and for every arrow that is held,
        it creates the middle section by taking in account the time that
        each arrow is held for. The image for the middle parts is saved
        in the list,HELDARROWLIST.
        

    '''
    for i in range(len(ARROWLIST)):
        if next_arrow_to_press <= len(ARROWLIST):        
            if len(ARROWLIST[i]) == 3:
                timeDifference = ARROWLIST[i][2] - ARROWLIST[i][1]
                yValueHold = HOLDPICTUREHEIGHT*(timeDifference/((HOLDPICTUREHEIGHT/ARROWTRAVELDIST)*SPEED))
                if ARROWLIST[i][0] == UP:
                    pixels = getPixelArray(HOLDUP)
                if ARROWLIST[i][0] == RIGHT:
                    pixels = getPixelArray(HOLDRIGHT)
                if ARROWLIST[i][0] == LEFT:
                    pixels = getPixelArray(HOLDLEFT)
                if ARROWLIST[i][0] == DOWN:
                    pixels = getPixelArray(HOLDDOWN)
        
                pixels = pixels[:,:yValueHold,: ]
                holdImg = pygame.surfarray.make_surface(pixels)
                HELDARROWLIST.append(holdImg)
            else:
                HELDARROWLIST.append("none")
    return
def ExtractMusic():
    '''()->

        Opens arrowplacements.txt and stores the names, artists, and arrow placements for all difficulties in their proper lists.
        

    '''
    ARROWLIST = []
    f =  open("arrowplacements.txt")
    line = f.readline()
    line = line.replace('"', '').strip()
 

    while line != "":
        while line != "next":
            if line[:4] == "name":
                NAMESLIST.append(line[5:])
            if line[:4] == "arti":
                ARTLIST.append(line[5:])
            if line[:4] == "easy":
                EASYLIST.append(line[5:])
            if line[:4] == "medi":
                MEDLIST.append(line[5:])
            if line[:4] == "hard":
                HARDLIST.append(line[5:])
            if line[:4] == "insa":
                INSLIST.append(line[5:])

            line = f.readline()
            line = line.replace('"', '').strip()
        line = f.readline()
        line = line.replace('"', '').strip()
    return
def setArrowList(songnumber,difficulty):
    '''(int,int)-> list of list of intergers,string

    Take the song the user selected from songnumber and the difficulty and then uses them to set up the correct set of arrows from EASYLIST,MEDLIST,
    HARLIST or INSLIST to ARROWLIST.
    

        
    '''
    if difficulty == 1:
        ARROWLIST = EASYLIST[songnumber-1]
    if difficulty == 2:
        ARROWLIST = MEDLIST[songnumber-1]
    if difficulty == 3:
        ARROWLIST = HARDLIST[songnumber-1]
    if difficulty == 4:
        ARROWLIST = INSLIST[songnumber-1]
        ARROWLIST = str(ARROWLIST)
    ARROWLIST = literal_eval(ARROWLIST)
    songfilename = NAMESLIST[songnumber-1]
    return ARROWLIST,songfilename
        
def setVariables():
    '''
    ()-> int,list of list of intergers,list of intergers,interger,list of strings,interger,float,interger,interger,interger,interger,interger

    
    Defines all the variables used in playing game loop and returns them to the main() function.
    
        
    '''
    HELDARROWLIST = []
    ARROWCURRENTPOSLIST = []
    ARROWTRAVELDIST = ARROWHOLDERY-STARTINGPOSITION
    for i in range(len(ARROWLIST)):
        if ARROWLIST[i][0] == 'UP':
            ARROWLIST[i][0] = UP
        if ARROWLIST[i][0] == 'DOWN':
            ARROWLIST[i][0] = DOWN
        if ARROWLIST[i][0] == 'RIGHT':
            ARROWLIST[i][0] = RIGHT
        if ARROWLIST[i][0] == 'LEFT':
            ARROWLIST[i][0] = LEFT
    arrowHitResult = []
    for item in ARROWLIST:
        ARROWCURRENTPOSLIST.append(-500.00)
        arrowHitResult.append(N)
    passingpoints = 50
    currentArrow = 0
    time = 0
    next_arrow_to_press = 0
    next_arrow_to_hold = 0
    next_held_arrow = 0
    nextHoldValue = 0
    score = 0
    return passingpoints,HELDARROWLIST,ARROWCURRENTPOSLIST,ARROWTRAVELDIST,arrowHitResult,currentArrow,time,next_arrow_to_press,next_arrow_to_hold,next_held_arrow,nextHoldValue,score


def getPixelArray(filename):
    '''
    (filename)-> image
    Take a image based on the file name inputted and converts it into a Pixel array.
    '''
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    
    return pygame.surfarray.array3d(image)

def check_if_arrow_hit_press(next_arrow_to_press,score,arrowdirection,next_arrow_to_hold,passingpoints):
    '''
     (interger,interger,image,interger,interger)-> interger,interger,image,interger,interger

      Takes the arrow that should be pressed next and checks how far the arrow is from its destination at the time of the click. Gives appropriate score
      based on how close the player was and if they click when there was no arrow there, they loose score. Changes the next arrow to one greater. It also
      sets next_arrow_to_hold to the next arrow if no arrow is being held or if the next arrow is held. Adds 2 to passingpoints if they successfully hit
      the arrow which is the variable that monitors how close the player is to failing.
     
    '''
    if ARROWHOLDERY - 15 < (ARROWCURRENTPOSLIST[next_arrow_to_press]) and  ARROWHOLDERY + 15 > (ARROWCURRENTPOSLIST[next_arrow_to_press]) and ARROWLIST[next_arrow_to_press][0] == arrowdirection:            
        score += 300
        passingpoints += 2
        arrowHitResult[next_arrow_to_press] = A
        
        if len(ARROWLIST[next_arrow_to_press]) == 2:
            ARROWCURRENTPOSLIST[next_arrow_to_press] = 1500
            if len(ARROWLIST[next_arrow_to_hold]) == 2:
                next_arrow_to_hold = next_arrow_to_press    
        if len(ARROWLIST[next_arrow_to_press]) == 3:
            next_arrow_to_hold = next_arrow_to_press
        next_arrow_to_press += 1    
        
    elif ARROWHOLDERY - 25 < (ARROWCURRENTPOSLIST[next_arrow_to_press]) and  ARROWHOLDERY + 25> (ARROWCURRENTPOSLIST[next_arrow_to_press]) and ARROWLIST[next_arrow_to_press][0] == arrowdirection:
        score += 100
        passingpoints += 2
        arrowHitResult[next_arrow_to_press] = B
        
        if len(ARROWLIST[next_arrow_to_press]) == 2:
            ARROWCURRENTPOSLIST[next_arrow_to_press] = 1500
            if len(ARROWLIST[next_arrow_to_hold]) == 2:
                next_arrow_to_hold = next_arrow_to_press 
        if len(ARROWLIST[next_arrow_to_press]) == 3:
            next_arrow_to_hold = next_arrow_to_press
        next_arrow_to_press += 1    
    elif ARROWHOLDERY - 40 < (ARROWCURRENTPOSLIST[next_arrow_to_press]) and  ARROWHOLDERY + 40> (ARROWCURRENTPOSLIST[next_arrow_to_press]) and ARROWLIST[next_arrow_to_press][0] == arrowdirection:
        score += 50
        passingpoints += 2
        arrowHitResult[next_arrow_to_press] = C
        if len(ARROWLIST[next_arrow_to_press]) == 2:
            ARROWCURRENTPOSLIST[next_arrow_to_press] = 1500
            if len(ARROWLIST[next_arrow_to_hold]) == 2:
                next_arrow_to_hold = next_arrow_to_press 
        if len(ARROWLIST[next_arrow_to_press]) == 3:
            next_arrow_to_hold = next_arrow_to_press
        next_arrow_to_press += 1    
    else:
            score = score - 10
    return next_arrow_to_press,score,next_arrow_to_hold,passingpoints

def check_if_arrow_hit_hold(next_arrow_to_hold,score,arrowdirection,next_arrow_to_press,passingpoints):
    '''
     (interger,interger,image,interger,interger)-> interger,interger,image,interger,interger

      Takes the arrow that should be held next and checks how far the arrow is from its destination at the time of the release of the hold.
      Gives appropriate score based on how close the player. Changes the next hold to next arrow to press which will be the next arrow in the game.
       Adds 2 to passingpoints if they successfully hit the arrow which is the variable that monitors how close the player is to failing.
     
    '''
    timeDifference = ARROWLIST[next_arrow_to_hold][2] - ARROWLIST[next_arrow_to_hold][1]
    endOfHold = ARROWCURRENTPOSLIST[next_arrow_to_hold]-ARROWTRAVELDIST/SPEED*timeDifference

    if ARROWHOLDERY - 15 < (endOfHold) and  ARROWHOLDERY + 15 > (endOfHold) and ARROWLIST[next_arrow_to_hold][0] == arrowdirection:
        score += 300
        passingpoints += 2
        try:
            if ARROWLIST[next_arrow_to_hold][2] == ARROWLIST[next_arrow_to_hold - 1][2]:
                score+=300
                passingpoints += 2
                ARROWCURRENTPOSLIST[next_arrow_to_hold-1] = 1500
        except:
            pass
            
        ARROWCURRENTPOSLIST[next_arrow_to_hold] = 1500
        next_arrow_to_hold = next_arrow_to_press                
        
    elif ARROWHOLDERY - 25 < (endOfHold) and  ARROWHOLDERY + 25> (endOfHold) and ARROWLIST[next_arrow_to_hold][0] == arrowdirection:
        score += 100
        passingpoints += 2
        try:
            if ARROWLIST[next_arrow_to_hold][2] == ARROWLIST[next_arrow_to_hold - 1][2]:
                score+=100
                passingpoints += 2
                ARROWCURRENTPOSLIST[next_arrow_to_hold-1] = 1500
        except:
            pass
        ARROWCURRENTPOSLIST[next_arrow_to_hold] = 1500
        next_arrow_to_hold = next_arrow_to_press
        

    elif ARROWHOLDERY - 40 < (endOfHold) and  ARROWHOLDERY + 40> (endOfHold) and ARROWLIST[next_arrow_to_hold][0] == arrowdirection:
        score += 50
        passingpoints += 2
        try:
            if ARROWLIST[next_arrow_to_hold][2] == ARROWLIST[next_arrow_to_hold - 1][2]:
                score+=50
                passingpoints += 2
                ARROWCURRENTPOSLIST[next_arrow_to_hold-1] = 1500
        except:
            pass
        ARROWCURRENTPOSLIST[next_arrow_to_hold] = 1500
        next_arrow_to_hold = next_arrow_to_press
        
    elif ARROWHOLDERY < ARROWCURRENTPOSLIST[next_arrow_to_hold]:
        ARROWCURRENTPOSLIST[next_arrow_to_hold] = 1500
        next_arrow_to_hold = next_arrow_to_press
    return next_arrow_to_press,score,next_arrow_to_hold,passingpoints


def set_arrow_to_start(currentArrow,time):
    '''
     (interger,float)-> interger
    Sets the currentArrow to starting position if it is time for it to begin dropping on the screen. currentArrow determines which arrow is being dropped
    next.
       
    '''

    for i in range(4):
        if round(time,2) == round((ARROWLIST[currentArrow][1] - SPEED),2):
            ARROWCURRENTPOSLIST [currentArrow] = STARTINGPOSITION
            if currentArrow < len(ARROWLIST) - 1:
                currentArrow += 1
              
    return currentArrow


                    
                    
def MoveArrows():
    '''
    ()-> 
    For every arrow that is in ARROWLIST and on the screen, the position of the arrows is moved down the necessary amount and changed in the y coordinate
    list, ARROWCURRENTPOS. The arrows are then drawn on the screen in their new posititons. If the arrows are holding arrows, 2 arrows are drawn,one at the
    start of the hold and one at the end of the hold. The middle section is also drawn taking from the list of pictures, HELDARROWLIST.
    '''
    for i in range(len(ARROWCURRENTPOSLIST)):
        if ARROWCURRENTPOSLIST[i] < 1499 and ARROWCURRENTPOSLIST[i] > -500:
            if len(ARROWLIST[i]) == 2:
                    
                ARROWCURRENTPOSLIST[i] = ARROWCURRENTPOSLIST[i] + ((ARROWTRAVELDIST)/(SPEED * FPS))
                if ARROWLIST[i][0] == UP:
                    DISPLAYSURF.blit(ARROWLIST[i][0], (UPARROWX, ARROWCURRENTPOSLIST[i]))
                if ARROWLIST[i][0] == LEFT:
                    DISPLAYSURF.blit(ARROWLIST[i][0], (LEFTARROWX, ARROWCURRENTPOSLIST[i]))
                if ARROWLIST[i][0] == DOWN:
                    DISPLAYSURF.blit(ARROWLIST[i][0], (DOWNARROWX, ARROWCURRENTPOSLIST[i]))
                if ARROWLIST[i][0] == RIGHT:
                    DISPLAYSURF.blit(ARROWLIST[i][0], (RIGHTARROWX, ARROWCURRENTPOSLIST[i]))                    

            if len(ARROWLIST[i]) == 3:
                timeDifference = ARROWLIST[i][2] - ARROWLIST[i][1]
                
                ARROWCURRENTPOSLIST[i] = ARROWCURRENTPOSLIST[i] + ((ARROWTRAVELDIST)/(SPEED * FPS))
                if ARROWLIST[i][0] == UP:                    
                    DISPLAYSURF.blit(HELDARROWLIST[i], (UPARROWX + 12, 40 + ARROWCURRENTPOSLIST[i]-ARROWTRAVELDIST/SPEED*timeDifference))
                    DISPLAYSURF.blit(ARROWLIST[i][0], (UPARROWX, ARROWCURRENTPOSLIST[i]-ARROWTRAVELDIST/SPEED*timeDifference))
                    DISPLAYSURF.blit(ARROWLIST[i][0], (UPARROWX, ARROWCURRENTPOSLIST[i]))
                    
                if ARROWLIST[i][0] == LEFT:
                    DISPLAYSURF.blit(HELDARROWLIST[i], (LEFTARROWX + 10, 40 + ARROWCURRENTPOSLIST[i]-ARROWTRAVELDIST/SPEED*timeDifference))
                    DISPLAYSURF.blit(ARROWLIST[i][0], (LEFTARROWX, ARROWCURRENTPOSLIST[i]-ARROWTRAVELDIST/SPEED*timeDifference))
                    DISPLAYSURF.blit(ARROWLIST[i][0], (LEFTARROWX, ARROWCURRENTPOSLIST[i]))
                if ARROWLIST[i][0] == DOWN:
                    DISPLAYSURF.blit(HELDARROWLIST[i], (DOWNARROWX + 12, 40 + ARROWCURRENTPOSLIST[i]-ARROWTRAVELDIST/SPEED*timeDifference))
                    DISPLAYSURF.blit(ARROWLIST[i][0], (DOWNARROWX, ARROWCURRENTPOSLIST[i]-ARROWTRAVELDIST/SPEED*timeDifference))
                    DISPLAYSURF.blit(ARROWLIST[i][0], (DOWNARROWX, ARROWCURRENTPOSLIST[i]))
                if ARROWLIST[i][0] == RIGHT:
                    DISPLAYSURF.blit(HELDARROWLIST[i], (RIGHTARROWX + 10, 40 + ARROWCURRENTPOSLIST[i]-ARROWTRAVELDIST/SPEED*timeDifference))
                    DISPLAYSURF.blit(ARROWLIST[i][0], (RIGHTARROWX, ARROWCURRENTPOSLIST[i]-ARROWTRAVELDIST/SPEED*timeDifference))
                    DISPLAYSURF.blit(ARROWLIST[i][0], (RIGHTARROWX, ARROWCURRENTPOSLIST[i])) 
                
                
                
        if ARROWCURRENTPOSLIST[i] > 1500:
            ARROWCURRENTPOSLIST[i] = 1500
    return

FPS = 25 # frames per second setting
HOLDPICTUREHEIGHT = 1800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
songNumber = 0
passingpoints = 0
menusnd = pygame.mixer.Sound('move_cursor.ogg')
slctsnd = pygame.mixer.Sound('select.ogg')
music1 = pygame.mixer.Sound('select.ogg')
ARROWHOLDER = pygame.image.load('Arrow_Holder.png')
RIGHT= pygame.image.load('Right_Arrow.png')
UP= pygame.image.load('Up_Arrow.png')
DOWN= pygame.image.load('Down_Arrow.png')
LEFT = pygame.image.load('Left_Arrow.png')
TITLEBACKGROUND = pygame.image.load('titleBackground.png')
HOLDDOWN = 'DOWNHOLD.png'
HOLDUP = 'UPHOLD.png'
HOLDLEFT = 'LEFTHOLD.png'
HOLDRIGHT = 'RIGHTHOLD.png'
TXTARROWHERO = pygame.image.load('txtArrowHero.png')
TXTSLCTMENU = pygame.image.load('txtSelectMusic.png')
HoldImageLoaded = False
font = pygame.font.SysFont("monospace", 76)
font1 = pygame.font.SysFont("monospace", 44)
font2 = pygame.font.SysFont("monospace", 16)
font3 = pygame.font.SysFont("monospace", 22)
font4 = pygame.font.SysFont("Viner Hand ITC", 200)
font5 = pygame.font.SysFont("monospace", 60)
mode = "title"
songpage = 0
DANCE = pygame.image.load("dancing.gif")
BACKGROUND = pygame.image.load("DDRBackground2.jpg")
BACKGROUND2 = pygame.image.load("DDRBackground1.jpg")
HIGHLIGHT  = pygame.image.load("highlight.png")
HIGHLIGHTLIST = [(67,152),(436,154),(64,382),(437,382)]
TITLELABELS = ["Play","Songs","Credits","Exit"]
DIFFICULTYLABELS = ["Easy","Medium","Hard","Insane"]
RESULTPAGELIST2 = ["Missed:","Longest Streak:","Hit Percentage:"]
RESULTPAGELIST1 = ["Awesome:","Great:","OK:"]
RESULTSCOOR = [(290,180),(290,220),(290,260),(650,180),(650,220),(650,260)]
RESULTSACT = [1,2,3,4,5,6]
TITLELABELSCOOR = [(160,222),(520,222),(124,452),(540,452)]
SONGLABELSCOOR = [(120,222),(489,222),(124,452),(495,452)]
DIFFICULTIESCOOR = [(160,222),(510,222),(160,452),(510,452)]
NACOOR = [(135,222),(515,222),(135,452),(515,452)]
ARROWLIST = []
NAMESLIST = []
EASYLIST = []
MEDLIST = []
HARDLIST = []
INSLIST = []
ARTLIST = []

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
SPEED = 2
STARTINGPOSITION = -80.00
endOfHold = 0
hoveringOver = 1








ExtractMusic()
pygame.time.wait(2000)

fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('Arrow Hero')









while True: # the full game loop
    
    while mode == "title":

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(TITLEBACKGROUND, (0,0))
        DISPLAYSURF.blit(TXTARROWHERO, (180,25))
        DISPLAYSURF.blit(HIGHLIGHT, HIGHLIGHTLIST[hoveringOver-1])
        label = font2.render('|<>^ - Move|Enter - Select|Backspace - Back|', 1, (255,255,255))
        DISPLAYSURF.blit(label, (180,125))
        for i in range(len(TITLELABELS)):
            label = font1.render(str(TITLELABELS[i]), 1, (255,255,255))
            DISPLAYSURF.blit(label, (TITLELABELSCOOR[i]))

        
        
        
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                  
                if event.key == K_UP:
  
                    if hoveringOver == 3:
                        hoveringOver = 1
                    if hoveringOver == 4:
                        hoveringOver = 2

                if event.key == K_DOWN:
 
                    if hoveringOver == 1:
                        hoveringOver = 3
                    if hoveringOver == 2:
                        hoveringOver = 4

                if event.key == K_LEFT:

                    if hoveringOver == 2:
                        hoveringOver = 1
                    if hoveringOver == 4:
                        hoveringOver = 3

                if event.key == K_RIGHT:

                    if hoveringOver == 1:
                        hoveringOver = 2
                    if hoveringOver == 3:
                        hoveringOver = 4
                if event.key == K_RETURN:
                    slctsnd.play()
                    if hoveringOver == 1:
                        mode = "select music"
                        music1 = pygame.mixer.Sound(NAMESLIST[(songpage*4)-1+hoveringOver])
                        music1.play(0)
                    if hoveringOver ==3:
                        mode = "credits"
                    if hoveringOver ==2:
                        mode = "songs" 
                    if hoveringOver == 4:
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
    while mode == "credits":

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(BACKGROUND2, (0,0))
        DISPLAYSURF.blit(TXTARROWHERO, (180,25))
 
        label = font2.render('|<>^ - Move|Enter - Select|Backspace - Back|', 1, (255,255,255))
        DISPLAYSURF.blit(label, (180,125))
        label = font3.render('Software Developped By: Nikola Andrejevic', 1, (255,255,255))
        DISPLAYSURF.blit(label, (140,200))
        label = font3.render('Institution: Humberside C.I.', 1, (255,255,255))
        DISPLAYSURF.blit(label, (140,240))
        label = font3.render('Release Date:June 1rst, 2013.', 1, (255,255,255))
        DISPLAYSURF.blit(label, (140,280))
              
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    mode = "title" 

            pygame.display.update()
            
    while mode == "songs":

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(BACKGROUND2, (0,0))
        DISPLAYSURF.blit(TXTARROWHERO, (180,25))
 
        label = font2.render('|<>^ - Move|Enter - Select|Backspace - Back|', 1, (255,255,255))
        DISPLAYSURF.blit(label, (180,125))
        for i in range(8):
            label = font3.render(str(NAMESLIST[i][:-4]), 1, (255,255,255))
            DISPLAYSURF.blit(label, (110,200+(i*40)))
        for i in range(8,16):
            try:
                label = font3.render(str(NAMESLIST[i][:-4]), 1, (255,255,255))
                DISPLAYSURF.blit(label, (400,100+(i*40)))
            except:
                pass
              
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    mode = "title" 

            pygame.display.update() 
    while mode == "select music":
        highscoresdone = False
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(TITLEBACKGROUND, (0,0))
        DISPLAYSURF.blit(TXTSLCTMENU, (180,25))
        DISPLAYSURF.blit(HIGHLIGHT, HIGHLIGHTLIST[hoveringOver-1])
        label = font2.render('|<>^ - Move|Enter - Select|Backspace - Back|', 1, (255,255,255))
        DISPLAYSURF.blit(label, (180,125))
        for i in range(len(TITLELABELS)):
            try:
                label = font2.render(str(NAMESLIST[songpage*4+i][:-4]), 1, (255,255,255))
                DISPLAYSURF.blit(label, (SONGLABELSCOOR[i]))
                label = font2.render("By: " + str(ARTLIST[songpage*4+i]), 1, (255,255,255))
                DISPLAYSURF.blit(label, (SONGLABELSCOOR[i][0],SONGLABELSCOOR[i][1]+30))
            except:
                pass

        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:      
                if event.key == K_BACKSPACE:
                    music1.stop()
                    mode = "title"

                if event.key == K_UP:
                    if hoveringOver == 1 or hoveringOver == 2:
                        if songpage > 0:
                            songpage -= 1
                    elif hoveringOver == 3:
                        hoveringOver = 1
                    elif hoveringOver == 4:
                        hoveringOver = 2 
                    music1.stop()
                    music1 = pygame.mixer.Sound(NAMESLIST[(songpage*4)-1+hoveringOver])
                    music1.play(0)

                    

                if event.key == K_DOWN:
                    if hoveringOver == 3 or hoveringOver == 4:
                        if songpage < (len(NAMESLIST)-1)/4:
                            songpage += 1
                            hoveringOver = 1
                    elif hoveringOver == 1:
                        hoveringOver = 3
                    elif hoveringOver == 2:
                        hoveringOver = 4
                    music1.stop()
                    music1 = pygame.mixer.Sound(NAMESLIST[(songpage*4)-1+hoveringOver])
                    music1.play(0)
                    

                if event.key == K_LEFT:
                    if hoveringOver == 1:
                        if songpage > 0:
                            songpage -= 1
                            hoveringOver = 4
                    elif hoveringOver == 2:
                        hoveringOver = 1
                    elif hoveringOver == 3:
                        hoveringOver = 2
                    elif hoveringOver == 4:
                        hoveringOver = 3
                    music1.stop()
                    music1 = pygame.mixer.Sound(NAMESLIST[(songpage*4)-1+hoveringOver])
                    music1.play(0)
                    

                        

                if event.key == K_RIGHT:
                
                    if hoveringOver == 4:
                        if songpage < (len(NAMESLIST)-1)/4:
                            songpage += 1
                            hoveringOver = 1
                    elif hoveringOver == 3:
                        hoveringOver = 4       
                    elif hoveringOver == 2:
                        hoveringOver = 3        
                    elif hoveringOver == 1:
                        hoveringOver = 2
                    music1.stop()
                    music1 = pygame.mixer.Sound(NAMESLIST[(songpage*4)-1+hoveringOver])
                    music1.play(0)

                if event.key == K_RETURN:
                    slctsnd.play()
                    mode = "select difficulty"
                    songNumber = (songpage*4)-1+hoveringOver 
                    
            pygame.display.update()

    while mode == "select difficulty":
        

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(TITLEBACKGROUND, (0,0))
        DISPLAYSURF.blit(TXTSLCTMENU, (180,25))
        DISPLAYSURF.blit(HIGHLIGHT, HIGHLIGHTLIST[hoveringOver-1])
        label = font2.render('|<>^ - Move|Enter - Select|Backspace - Back|', 1, (255,255,255))
        DISPLAYSURF.blit(label, (180,125))
        for i in range(4):
            if [EASYLIST,MEDLIST,HARDLIST,INSLIST][i][songNumber] != "none":

                label = font1.render(str(DIFFICULTYLABELS[i]), 1, (255,255,255))
                DISPLAYSURF.blit(label, (DIFFICULTIESCOOR[i]))
            else:
                label = font3.render("Not Available", 1, (255,255,255))
                DISPLAYSURF.blit(label, (NACOOR[i]))
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    music1.stop()
                    mode = "select music" 
                if event.key == K_UP:

                    if hoveringOver == 3:
                        hoveringOver = 1
                    if hoveringOver == 4:
                        hoveringOver = 2

                if event.key == K_DOWN:

                    if hoveringOver == 1:
                        hoveringOver = 3
                    if hoveringOver == 2:
                        hoveringOver = 4

                if event.key == K_LEFT:

                    if hoveringOver == 2:
                        hoveringOver = 1
                    if hoveringOver == 4:
                        hoveringOver = 3

                if event.key == K_RIGHT:
                    if hoveringOver == 1:
                        hoveringOver = 2
                    if hoveringOver == 3:
                        hoveringOver = 4
                if event.key == K_RETURN:
                    if [EASYLIST,MEDLIST,HARDLIST,INSLIST][hoveringOver-1][songNumber] != "none":
                        slctsnd.play()
                        music1.stop()

                        
                        ARROWLIST,songfilename = setArrowList(songNumber+1,hoveringOver)
                        passingpoints,HELDARROWLIST,ARROWCURRENTPOSLIST,ARROWTRAVELDIST,arrowHitResult,currentArrow,time,next_arrow_to_press,next_arrow_to_hold,next_held_arrow,nextHoldValue,score = setVariables()

                        pygame.mixer.music.load(songfilename)
                        MakeHeldArrowList()
                        mode = "game"

                        pygame.time.wait(2000)
                    
                        

        pygame.display.update()


    while mode == "game":
        
        pygame.mixer.music.play(0,time)
        
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(BACKGROUND, (0,0))
        DISPLAYSURF.blit(ARROWHOLDER, (ARROWHOLDERX, ARROWHOLDERY))

        
        #dance.blit(DISPLAYSURF, (0, 0))
        try:
            if len(ARROWLIST[next_arrow_to_press]) == 3:
                timeDifference = ARROWLIST[next_arrow_to_press][2] - ARROWLIST[next_arrow_to_press][1]
                endOfHold = ARROWCURRENTPOSLIST[next_arrow_to_press]-ARROWTRAVELDIST/SPEED*timeDifference
        except:
            pass
        currentArrow = set_arrow_to_start(currentArrow,time)
        MoveArrows()   


        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN and next_arrow_to_press < len(ARROWLIST):
                if event.key == K_UP or K_DOWN or K_LEFT or K_RIGHT:
                
                    if event.key == K_UP:
                        next_arrow_to_press,score,next_arrow_to_hold,passingpoints = check_if_arrow_hit_press(next_arrow_to_press,score,UP,next_arrow_to_hold,passingpoints)

                    if event.key == K_DOWN:
                        next_arrow_to_press,score,next_arrow_to_hold,passingpoints = check_if_arrow_hit_press(next_arrow_to_press,score,DOWN,next_arrow_to_hold,passingpoints)

                    if event.key == K_LEFT:
                        next_arrow_to_press,score,next_arrow_to_hold,passingpoints = check_if_arrow_hit_press(next_arrow_to_press,score,LEFT,next_arrow_to_hold,passingpoints)

                    if event.key == K_RIGHT:
                        next_arrow_to_press,score,next_arrow_to_hold,passingpoints = check_if_arrow_hit_press(next_arrow_to_press,score,RIGHT,next_arrow_to_hold,passingpoints)


            if next_arrow_to_press < len(ARROWLIST):
                if event.type == KEYUP and len(ARROWLIST[next_arrow_to_hold]) == 3:    
                    if event.key == K_UP or K_DOWN or K_LEFT or K_RIGHT:    
                        if event.key == K_UP and ARROWLIST[next_arrow_to_hold][0] == UP:
                            next_arrow_to_press,score,next_arrow_to_hold,passingpoints = check_if_arrow_hit_hold(next_arrow_to_hold,score,UP,next_arrow_to_press,passingpoints)
                    
                        if event.key == K_DOWN and ARROWLIST[next_arrow_to_hold][0] == DOWN:
                            next_arrow_to_press,score,next_arrow_to_hold,passingpoints = check_if_arrow_hit_hold(next_arrow_to_hold,score,DOWN,next_arrow_to_press,passingpoints)

                        if event.key == K_LEFT and ARROWLIST[next_arrow_to_hold][0] == LEFT:
                            next_arrow_to_press,score,next_arrow_to_hold,passingpoints = check_if_arrow_hit_hold(next_arrow_to_hold,score,LEFT,next_arrow_to_press,passingpoints)

                        if event.key == K_RIGHT and ARROWLIST[next_arrow_to_hold][0] == RIGHT:
                            next_arrow_to_press,score,next_arrow_to_hold,passingpoints = check_if_arrow_hit_hold(next_arrow_to_hold,score,RIGHT,next_arrow_to_press,passingpoints)
                    

                         


                
                
        if next_arrow_to_press < len(ARROWLIST):
 
            if ARROWCURRENTPOSLIST[next_arrow_to_press] > ARROWHOLDERY + 40 and arrowHitResult[next_arrow_to_press] == N:
                passingpoints -= 5
                arrowHitResult[next_arrow_to_press] = F
                next_arrow_to_press += 1
                if len(ARROWLIST[next_arrow_to_hold]) == 2:
                    next_arrow_to_hold = next_arrow_to_press 
            if endOfHold > ARROWHOLDERY + 40 and arrowHitResult[next_arrow_to_press] == N and len(ARROWLIST[next_arrow_to_press]) == 3:
                arrowHitResult[next_arrow_to_press] = F
                next_arrow_to_hold = next_arrow_to_press 
         
        if next_arrow_to_press == len(ARROWLIST):
            pygame.time.wait(2000)
            pygame.mixer.music.stop()
            RESULTSACT,lettergrade = countResults()
            mode = "Results"

        if passingpoints <= 0:
            pygame.time.wait(1000)
            pygame.mixer.music.stop()
            RESULTSACT,lettergrade = countResults()
            mode = "Results"

        if passingpoints > 50:
            passingpoints = 50
        label = font.render(str(score), 1, (255,255,255))
        DISPLAYSURF.blit(label, (50,520))    

        pygame.display.update()
        fpsClock.tick(FPS)
        time += 1.00/FPS
        

    while mode == "Results":

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(BACKGROUND2, (0,0))
        DISPLAYSURF.blit(TXTARROWHERO, (180,25))
        label = font2.render('Press Any Key To Continue', 1, (255,255,255))
        DISPLAYSURF.blit(label, (280,125))
        displayResults(score,lettergrade)
        pygame.display.update()
        pygame.time.wait(5000)

        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                mode = "High Scores"
                if highscoresdone == False:
                    USERNAMELIST,HIGHSCORELIST = getHighScores(songNumber,score)
                highscoresdone = True

        pygame.display.update()

    while mode == "High Scores":

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(BACKGROUND2, (0,0))
        DISPLAYSURF.blit(TXTARROWHERO, (180,25))
        displayHighScores(USERNAMELIST,HIGHSCORELIST)
        
        label = font2.render('Press Any Key To Continue', 1, (255,255,255))


        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                mode = "select music" 
        pygame.display.update()



