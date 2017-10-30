import pygame
import random
import math
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import datetime
import matplotlib.pyplot as plt

# Affects Performance
POPULATION_SIZE = 500
MATING_POOL_PERCENTAGE = 0.05
MUTATION_RATE = 0.005

# Relates to Genetic Algorithm
AMOUNT_OF_MOVES = 2000
AMOUNT_OF_POPULATIONS = 1
MAP = 0
DRAW = 1

# Collison points for outside of track
Map = [[[1, 2, 22, 697], [19, 2, 864, 27], [856, 26, 27, 673], [221, 674, 641, 25],
        [198, 683, 24, 16], [13, 692, 191, 3], [21, 667, 28, 25], [49, 677, 12, 14],
        [61, 683, 11, 10], [23, 640, 10, 30], [33, 652, 7, 21], [257, 663, 89, 21], 
        [278, 651, 55, 16], [299, 639, 569, 36], [317, 624, 199, 40], [338, 612, 134, 41], 
        [353, 600, 95, 34], [371, 588, 54, 33], [385, 581, 24, 14], [772, 545, 89, 98], 
        [813, 496, 52, 54], [833, 461, 32, 42], [793, 520, 26, 38], [722, 592, 57, 54], 
        [747, 568, 35, 31], [689, 610, 40, 34], [648, 626, 44, 16], [846, 429, 23, 40], 
        [776, 22, 89, 114], [821, 128, 48, 56], [799, 127, 38, 35], [837, 179, 24, 35], 
        [848, 208, 15, 36], [789, 130, 14, 20], [753, 20, 31, 96], [727, 24, 32, 73], 
        [703, 24, 27, 64], [368, 20, 338, 63], [340, 24, 35, 33], [357, 48, 16, 22], 
        [314, 21, 32, 23], [15, 18, 45, 45], [52, 20, 37, 28], [84, 24, 32, 16], 
        [15, 57, 22, 25], [403, 79, 2, 199], [392, 76, 14, 42], [370, 251, 35, 26], 
        [380, 236, 24, 14], [390, 216, 35, 46], [400, 194, 43, 54], [401, 170, 59, 61], 
        [404, 80, 77, 125], [478, 76, 65, 72], [536, 68, 41, 48], [567, 76, 30, 26], 
        [462, 129, 51, 49], [506, 135, 24, 27], [472, 175, 25, 19], [534, 103, 24, 29], 
        [141, 167, 105, 360], [235, 400, 454, 64], [429, 387, 244, 92], [468, 376, 189, 114], 
        [501, 354, 136, 148], [536, 323, 51, 191], [569, 288, 0, 0], [571, 290, 142, 146], 
        [592, 264, 134, 147], [612, 242, 101, 191], [625, 227, 73, 221], [637, 213, 48, 254], 
        [714, 288, 24, 104], [523, 337, 15, 21], [556, 304, 27, 24], [579, 276, 24, 19], 
        [245, 364, 40, 40], [279, 380, 36, 24], [241, 332, 19, 40], [257, 348, 17, 18], 
        [161, 147, 115, 74], [200, 137, 66, 11], [182, 137, 10, 12], [149, 155, 13, 11], 
        [241, 218, 18, 21], [317, 391, 26, 13], [231, 443, 56, 52], [279, 452, 30, 29], 
        [233, 481, 33, 35], [149, 519, 39, 41], [177, 512, 42, 34], [236, 404, 0, 0], [509, 632, 48, 14]],
    ]
# Scoring path
goals = [[51, 108, 74, 528], [86, 56, 216, 63], [294, 75, 57, 174], [344, 131, 27, 67], [301, 248, 50, 65],
         [332, 288, 133, 51], [463, 238, 64, 78], [507, 194, 65, 74], [547, 148, 77, 71], [603, 113, 114, 59], 
         [696, 152, 51, 61], [731, 205, 39, 56], [753, 256, 48, 160], [743, 403, 17, 87], [697, 459, 53, 65], 
         [663, 489, 47, 76], [455, 525, 229, 59], [294, 504, 181, 56], [248, 540, 62, 71], [100, 582, 159, 63]]

#Populations holds all the he data to create all the cars and there driving techniques
class Population():
    #Pass in the varibles even though they are global to change it to run multiple populations at the same time 
    def __init__(self,POPULATION_SIZE,MATING_POOL_PERCENTAGE,AMOUNT_OF_MOVES,MUTATION_RATE):
        self.cars = []
        self.populationSize = POPULATION_SIZE
        self.matingPool = []
        self.maxFit = 0
        self.averageFitness = 0
        self.matingPoolPercentage = MATING_POOL_PERCENTAGE
        self.amountOfMoves = AMOUNT_OF_MOVES
        self.mutationRate = MUTATION_RATE

        for i in range(self.populationSize):
            self.cars.append(Car(self.amountOfMoves))

    #scores all the cars and normailses it
    def evaluate(self):
        global y1, y2

        self.maxFit = 0
        self.matingPool = []
        self.averageFitness = 0
        for i in self.cars:
            self.maxFit = max(self.maxFit, i.fitness)

        for i in self.cars:
            self.averageFitness += i.fitness
            i.fitness /= float(self.maxFit)

        print "Maxium Fitness: %d\nAverage Fitness: %d\n" %(self.maxFit*100, self.averageFitness/self.populationSize*100)
        y1.append(self.maxFit)
        y2.append(self.averageFitness/self.populationSize)

        # populates matingpool based on cars fitness
        for i in range(self.populationSize):
            n = self.cars[i].fitness * 100
            for j in range(int(n)):
                self.matingPool.append(self.cars[i])

    #Bredding is decided here
    def selection(self):

        self.cars = []
        #Mating pool is cut off to only the top X percentage of cars
        self.matingPool.sort(key=lambda x: x.fitness, reverse=True)
        self.matingPool = self.matingPool[:int(len(self.matingPool)*self.matingPoolPercentage)]

        # Creates a nw populations of cars based on previous generation
        for i in range(self.populationSize):
            parentA = random.choice(self.matingPool).dna
            parentB = random.choice(self.matingPool).dna

            child = Dna(parentA.cross_over(parentB),self.amountOfMoves)
            child.mutation()

            self.cars.append(Car(self.amountOfMoves,child))

    # Move the cars and do the collison calulations
    def run(self):
        for i in range(self.populationSize):
            self.cars[i].update()
    #Draws each car
    def draw(self):
        for i in range(self.populationSize):
            self.cars[i].draw()
    #tests is all the populations is dead
    def test_crash(self):
        alive = False
        for i in range(self.populationSize):
            if not self.cars[i].crashed:
                alive = True
        return alive

#Holds all the movements of the car stored as "Dna"
class Dna():
    def __init__(self, genes,AMOUNT_OF_MOVES):
        # Setting new genes if none already exist
        if genes:
            self.genes = genes
        else:
            self.genes = []
            for i in range(AMOUNT_OF_MOVES):
                self.genes.append([random.randint(-1,1)/10.0, 0.1])
    
    # Breeds the cars togther
    def cross_over(self, parter):
        self.newGenes = []
        cross = random.randint(0,1)

        # take altentating moves from the cars
        if cross == 0:
            self.newGenes = []
            for i in range(1,len(self.genes)-1,2):
                try:
                    self.newGenes.append(self.genes[i-1])
                    self.newGenes.append(parter.genes[i])
                except:
                    pass
        # Take a random mid point and split the parents genes
        else:
            mid = random.randint(0,len(self.genes))
            self.newGenes = self.genes[:mid] + parter.genes[mid:]
        return self.newGenes

    # Adds random Dna to the mix that was present in the intaial spawn
    def mutation(self):

        for i in range(len(self.genes)):
            if random.randint(0,100000)<=100000*MUTATION_RATE:
                self.genes[i]=[random.randint(-1,1)/10.0, 0.1]

class Car():
    # Each car holds all the stats related to it
    def __init__(self,AMOUNT_OF_MOVES,dna = None):
        self.x = 0
        self.y = 0
        self.angle = math.pi
        self.count = 0
        self.score = 0
        self.bottom = False
        self.top = True
        self.car = [(200 - carSize[0]) / 2 +
                   self.x, (800 - carSize[1]) / 2 + self.y, carSize[0], carSize[1]]
        self.crashed = False
        self.amountOfMoves = AMOUNT_OF_MOVES
        self.loop = self.amountOfMoves
        if dna != None:
            self.dna = dna
        else:
            self.dna = Dna([],self.amountOfMoves)
        self.fitness = 0
        self.center = 0
        self.count1 = 0

    # Score is weighted 5* compared to count 
    def calc_fitness(self):
        self.fitness = self.score*5
        self.fitness += self.count
    
    #Tests collisions with the edge of the map
    def collide(self):
        a = pygame.Rect(self.car)
        return a.collidelist(Map[MAP])
        
    # Does all the calculations of the car
    def update(self):
        if not self.crashed:
            self.movement = self.dna.genes[self.count%self.loop]
            self.angle += self.movement[0]

            self.car = [(200 - carSize[0]) / 2 +
                   self.x, (800 - carSize[1]) / 2 + self.y, carSize[0], carSize[1]]

            self.dist = math.hypot(self.car[0] + (self.car[2] / 2) - WIDTH / 2,
                                self.car[1] + (self.car[3] / 2) - HEIGHT / 2)
            
            self.x += (math.sin(self.angle) * 90 /
                    math.pi) * (self.movement[1])
            self.y += (math.cos(self.angle) * 90 /
                    math.pi) * (self.movement[1])
            
            

            if pygame.Rect(self.car).collidelist(goals)!=-1:
                self.score += 1
                
            if self.collide() != -1:
                self.crashed = True
                self.calc_fitness()
            if pygame.Rect(self.car).colliderect(pygame.Rect([100,400,1,1])) and self.count%self.loop>10:
                self.score *= 1.1
                self.loop = self.count+1
            
            self.count+=1
    
    # Draws if not crashed
    def draw(self):
        if not self.crashed:
            pygame.draw.rect(screen, WHITE, self.car)

# Pygame constants
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

lifespan = 0
# Matplotlib setup
y1 = []
y2 = []
y3 = []
for i in range(100):
    y3.append(5000)
BackGround = [pygame.image.load('background_image.jpg')]

cars = []
population = []
carSize = [5, 10]

# Creats the population
for i in range(AMOUNT_OF_POPULATIONS):
    population.append(Population(POPULATION_SIZE,MATING_POOL_PERCENTAGE,AMOUNT_OF_MOVES,MUTATION_RATE))
generation = 1

#Setting up graph
plt.ion()
plt.title("Populations Fitness")
plt.plot(y1,"C1",label="Max Fitness")
plt.plot(y2,"C2",label="Average Fitness")
plt.plot(y3,"C3",label="Goal Fitness")
plt.legend()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key==32:
                DRAW = not DRAW
    # Runs each population 
    for i in range(len(population)):
        population[i].run()
        if not population[i].test_crash() or lifespan==AMOUNT_OF_MOVES:
            print "Generation: %d" %generation
            y3.append(5000)
            population[i].evaluate()
            population[i].selection()                
            plt.plot(y1,"C1",label="Max Fitness")
            plt.plot(y2,"C2",label="Average Fitness")
            plt.plot(y3,"C3",label="Goal Fitness")
            plt.ylabel('Fitness')
            plt.pause(0.05)
            generation+=1
            lifespan = 0
    # Drawing
    # Stops drawing to speed up sketch
    if DRAW:
        screen.blit(BackGround[MAP], [0,0])
        for i in population:
            i.draw()

        pygame.display.flip()
        clock.tick(60)
    lifespan+=1
pygame.quit()

while True:
    try:
        plt.pause(0.05)
    except:
        break


