'''
Translated from https://github.com/shiffman/The-Nature-of-Code-Examples/tree/master/chp09_ga/GA_Shakespeare_fancyfitness JS to python
'''
import random
from sys import stdin, stdout

def mapuj(a = 0.0, b = 1.0):
    return (a / b)**(1/2.0)


class DNA:
    genes = ""
    fitness = 0.0

    def __init__(self, num):
        self.num = num
        for i in range(num):
            self.genes += chr(random.randint(32, 126))

    def getPhrase(self):
        return self.genes

    def setFitness(self, target):
        score = 0
        for i in range(self.num):
            if target[i] == self.genes[i]:
                score += 1
        self.fitness = score**2

    def crossover(self, partner):
        child = DNA(self.num)
        midpoint = random.randint(0, self.num-1)
        temp = []
        for i in range(self.num):
            if i > midpoint:
                temp.append(self.genes[i])
            else:
                temp.append(partner.genes[i])

        child.genes = ''.join(temp)
        return child

    def mutate(self, mutationRate):
        temp = list(self.genes)
        for i in range(len(self.genes)):
            if random.random() < mutationRate:
                temp[i] = chr(random.randint(32,126))
                self.genes = ''.join(temp)

class Population:
    population = []
    matingPool = []
    finished = False
    generations = 0
    def __init__(self, targetPhrase, mutation = 0.01, popNum = 100):
        self.targetPhrase = targetPhrase
        self.mutation = mutation
        self.popNum = popNum
        for i in range(popNum):
            self.population.append(DNA(len(targetPhrase)))
        self.calcFitness()
        self.perfectScore = len(targetPhrase)**2


    def calcFitness(self):
        for i in range(self.popNum):
            self.population[i].setFitness(self.targetPhrase)

    def naturalSelection(self):
        matingPool = []
        maxFitness = 0.0
        for p in self.population:
            if p.fitness > maxFitness:
                maxFitness = p.fitness
        for p in self.population:
            fitness = mapuj(p.fitness, maxFitness)
            n = int(fitness * 100)
            for i in range(n):
                self.matingPool.append(p)

    def generate(self):
        for i in range(self.popNum):
            a = random.randint(0, len(self.matingPool)-1)
            b = random.randint(0, len(self.matingPool)-1)
            partnerA = self.matingPool[a]
            partnerB = self.matingPool[b]
            child = partnerA.crossover(partnerB)
            child.mutate(self.mutation)
            self.population[i] = child
        self.generations += 1

    def getBest(self):
        bestScore = 0
        index = 0
        for p in self.population:
            if p.fitness > bestScore:
                bestScore = p.fitness
                bestOne = p
        if bestScore == self.perfectScore:
            self.finished = True
        return bestOne.getPhrase()

    def getAverageFitness(self):
        total = 0.0
        for p in self.population:
            total += p.fitness
        return ((total/len(self.population)/self.perfectScore)**(1/2.0))*100

    def displaySomeOfPop(self):
        everything = ""
        dispLimit = min(self.popNum, 50)
        for i in range(dispLimit):
            everything += self.population[i].getPhrase() + "\t"
        return everything

def setup():
    global popMax
    popMax = 500
    global mutationRate
    mutationRate = 0.02
    global targetPhrase
    targetPhrase = "To be or not to be"
    global population
    population = Population(targetPhrase, mutationRate, popMax)

def displayInfo():
    global population
    global popMax
    global targetPhrase
    stdout.write( "Target phrase: " + targetPhrase+ "\n")
    stdout.write( "Best phrase:   " + population.getBest()+ "\n")
    stdout.write( "Average fitness: " + str(round(population.getAverageFitness(), 2)) + "%"+ "\n")
    stdout.write( "Total generations: " + str(population.generations)+ "\n")
    stdout.write( "Total population: " + str(popMax)+ "\n")
    stdout.write( "Mutation rate: " + str(mutationRate*100) + "%"+ "\n")
    stdout.write( "Phrases:\n" + population.displaySomeOfPop() + "\n"+ "\n")

def draw():
    global population
    displayInfo()
    population.naturalSelection()
    population.generate()
    population.calcFitness()


setup()
auto = False
while not population.finished:
    draw()
    if not auto:
        if raw_input("Press any key to process to next generation... ") == "auto":
            auto = True
raw_input("Genetic finding has ended. Press enter to exit program... ")
