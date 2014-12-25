#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Dragan
#
# Created:     09/05/2013
# Copyright:   (c) Dragan 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pygame, sys
from pygame.locals import *

def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((390, 390))
    pygame.display.set_caption('Hello World!')

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    listOfAvailableFonts = pygame.font.get_fonts()
    listOfLikedFonts = []
    fontSize = 12

    counter = 0
    nextFont = 0

    while True:
        DISPLAYSURF.fill(BLACK)

        fontName = pygame.font.match_font(listOfAvailableFonts[counter])

        fontObj = pygame.font.Font(fontName, fontSize)
        textSurfaceObject = fontObj.render('Hello World!', True, BLACK, WHITE)

        DISPLAYSURF.blit(textSurfaceObject, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                print listOfLikedFonts
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_UP:
                    counter += 1
                    print 'Font name:' + listOfAvailableFonts[counter] + '   Font Number:', counter, 'out of', len(listOfAvailableFonts), 'fonts!'
                if event.key == K_DOWN:
                    counter -= 1
                    print 'Font name:' + listOfAvailableFonts[counter] + '   Font Number:', counter, 'out of', len(listOfAvailableFonts), 'fonts!'
                if event.key == K_LEFT:
                    fontSize -= 1
                    print 'Font size:', fontSize
                if event.key == K_RIGHT:
                    fontSize += 1
                    print 'Font size:', fontSize
                if event.key == K_SPACE:
                    listOfLikedFonts.append([listOfAvailableFonts[counter], fontSize])


        pygame.display.update()

    pass

if __name__ == '__main__':
    main()
