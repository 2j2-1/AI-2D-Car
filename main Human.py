import pygame
import random
import math
pygame.init()

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
SIZE = [640, 640]
WIDTH = SIZE[0]
HEIGHT = SIZE[1]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Car GA")
clock = pygame.time.Clock()
carSize = [5, 10]
movement = [0, 0, 0, 0]
x, y = 0, 0
angle = math.pi / 2
done = False
score = 0
top = True
bottom = False

def scorer(top, bottom, score):
    if pygame.Rect(car).colliderect(pygame.Rect((WIDTH / 2, 0, WIDTH / 2 + 1, 50))) and bottom:
        print "Score:", score+1
        return True,False,score+1
    if pygame.Rect(car).colliderect(pygame.Rect((WIDTH / 2, HEIGHT - 50, WIDTH / 2 + 1, HEIGHT))) and top:
        return False,True,score
    return top,bottom,score


def car_pos(carSize):
    return [(WIDTH - carSize[0]) / 2 + x, (50 - carSize[1]) / 2 + y, carSize[0], carSize[1]]

def new_ai(ai, count):
    if count > 20:
        ai = ai[:count - 20]
        print count
    else:
        print "New_ai"
        ai = []

    for i in range(1000 - count + 20):
        ai.append([random.randint(-1, 1) / 10.0, random.randint(-1, 1) /
                   10.0])
    return ai

count = 0
ai = new_ai([], 0)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == 119:
                movement[1] += 0.1
            if event.key == 97:
                movement[0] += 0.05
            if event.key == 115:
                movement[1] -= 0.1
            if event.key == 100:
                movement[0] -= 0.05
            print event.key
        if event.type == pygame.KEYUP:
            if event.key == 119:
                movement[1] = 0
            if event.key == 97:
                movement[0] = 0
            if event.key == 115:
                movement[1] = 0
            if event.key == 100:
                movement[0] = 0
        
    # movement = ai[count]

    angle += movement[0]
    x += (math.sin(angle) * 90 /
          math.pi) * (movement[1])
    y += (math.cos(angle) * 90 /
          math.pi) * (movement[1])
    car = car_pos(carSize)
    top,bottom,score = scorer(top,bottom,score)

    dist = math.hypot(car[0] + (car[2] / 2) - WIDTH / 2,
                      car[1] + (car[3] / 2) - HEIGHT / 2)

    
    if dist < HEIGHT / 2 - 50 or dist > HEIGHT / 2:
        print "out of bounds"
        ai = new_ai(ai, count)
        count = 0
        x = 0
        y = 0
        angle = math.pi / 2
        car = [(WIDTH - carSize[0]) / 2 +
               x, (50 - carSize[1]) / 2 + y, carSize[0], carSize[1]]
        score = 0

    #Drawing
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT / 2), HEIGHT / 2)
    pygame.draw.circle(screen, BLACK, (WIDTH / 2, HEIGHT / 2), HEIGHT / 2 - 1)
    pygame.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT / 2), HEIGHT / 2 - 50)
    pygame.draw.circle(screen, BLACK, (WIDTH / 2, HEIGHT / 2), HEIGHT / 2 - 51)
    pygame.draw.rect(screen, WHITE, car)

    pygame.display.flip()
    clock.tick(60)
    count += 1
pygame.quit()
