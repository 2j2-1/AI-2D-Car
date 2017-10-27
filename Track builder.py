import pygame
import random
import math
import datetime

pygame.init()
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
SIZE = [884, 700]
WIDTH = SIZE[0]
HEIGHT = SIZE[1]
MID = [WIDTH/2,HEIGHT/2]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Car GA")
clock = pygame.time.Clock()
done = False
BackGround = pygame.image.load('background_image.jpg')

newShape = True
startPos = 0,0
allRects = []
print str(datetime.datetime.now())
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            newShape = False
            startPos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            newShape = True
            a = startPos[0]
            b = startPos[1]
            c = endPos[0]-startPos[0]
            d = endPos[1]-startPos[1]
            if c<0:
                a,c = a+c,abs(c)
            if d<0:
                b,d = b+d,abs(d)

            allRects.append([a,b,c,d])
        try:
            endPos = event.pos
        except:
            pass

    screen.blit(BackGround, [0,0])

    if not newShape:
        pygame.draw.rect(screen,WHITE,(startPos[0],startPos[1],endPos[0]-startPos[0],endPos[1]-startPos[1]))
    for i in allRects:
        pygame.draw.rect(screen,WHITE,i)
    # Drawing

    pygame.display.flip()
    clock.tick(60)
print allRects
input()
pygame.quit()
