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


class Car():
    """docstring for car_Brain"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = math.pi / 2
        self.ai = self.new_ai([], 0)
        self.dist = 0
        self.count = 0

    def new_ai(self, ai, count):
        if count > 20:
            ai = ai[:count - 20]
            print count
        else:
            print "New_ai"
            ai = []

        for i in range(1000 - count + 20):
            ai.append([random.randint(0, 1) / 10.0, random.randint(0, 1) /
                       10.0, -random.randint(0, 1) / 10.0, -random.randint(0, 1) / 10.0])
        return ai

count = 0
cars = []
for i in range(10):
    cars.append(Car(x, y))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # if event.type == pygame.KEYDOWN:
        #     if event.key == 119:
        #         movement[0] += 0.1
        #     if event.key == 97:
        #         movement[1] += 0.05
        #     if event.key == 115:
        #         movement[2] -= 0.1
        #     if event.key == 100:
        #         movement[3] -= 0.05
        # if event.type == pygame.KEYUP:
        #     if event.key == 119:
        #         movement[0] = 0
        #     if event.key == 97:
        #         movement[1] = 0
        #     if event.key == 115:
        #         movement[2] = 0
        #     if event.key == 100:
        #         movement[3] = 0

            # Calculations
    # try:
    for i in cars:
        print i.count
        try:
        movement = i.ai[i.count]
        # except:
        # print "yeyeyey"
        i.angle += movement[1] + movement[3]
        i.x += (math.sin(angle) * 90 /
                math.pi) * (movement[0] + movement[2])
        i.y += (math.cos(angle) * 90 /
                math.pi) * (movement[0] + movement[2])
        car = [(WIDTH - carSize[0]) / 2 +
               x, (50 - carSize[1]) / 2 + y, carSize[0], carSize[1]]

        i.dist = math.hypot(car[0] + (car[2] / 2) - WIDTH / 2,
                            car[1] + (car[3] / 2) - HEIGHT / 2)

        if pygame.Rect(car).colliderect(pygame.Rect((WIDTH / 2, 0, WIDTH / 2 + 1, 50))) and bottom:
            score += 1
            print "Amount of Laps Completed %d" % score
            top = True
            bottom = False
        if pygame.Rect(car).colliderect(pygame.Rect((WIDTH / 2, HEIGHT - 50, WIDTH / 2 + 1, HEIGHT))) and top:
            top = False
            bottom = True
        if i.dist < HEIGHT / 2 - 50 or i.dist > HEIGHT / 2:
            print "out of bounds"
            del i

    # print x, y
    # Drawing
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT / 2), HEIGHT / 2)
    pygame.draw.circle(screen, BLACK, (WIDTH / 2, HEIGHT / 2), HEIGHT / 2 - 1)
    pygame.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT / 2), HEIGHT / 2 - 50)
    pygame.draw.circle(screen, BLACK, (WIDTH / 2, HEIGHT / 2), HEIGHT / 2 - 51)
    for i in cars:
        car = [(WIDTH - carSize[0]) / 2 +
               i.x, (50 - carSize[1]) / 2 + i.y, carSize[0], carSize[1]]
        pygame.draw.rect(screen, WHITE, car)
        i.count += 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
