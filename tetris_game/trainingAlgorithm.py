import math
import ai
import random
import numpy as np
from pprint import pprint
class trainingAlgorithm:
    def normalize(ai):
        norm = math.sqrt(ai.heightWeight**2 + ai.linesWeight**2 + ai.holesWeight**2 + ai.bumpinessWeight**2)
        ai.heightWeight /= norm
        ai.linesWeight /= norm
        ai.holesWeight /= norm
        ai.bumpinessWeight /= norm

    def generateNewAi():
        newAI = ai.AI(random.random(), 
              random.random(),
              random.random(), 
              random.random())
        trainingAlgorithm.normalize(newAI)
        return newAI
    
    def sort(allAi):
        sorted(allAi, key = lambda ai: ai.fitness, reverse = True)

    # def computeFitness(allAi, numberOfGames, maxNumberOfMoves):
    #     for ai in allAi :
    #         totalScore = 0
    #         for i in range(numberOfGames):
    #             score = 0
    def tournamentSelect(allAi):
        indices = np.randint(0,len(allAi)-1, len(allAi)//10)
        np.sort(indices)
        return [allAi[indices[0]],allAi[indices[1]]]
    
    def crossOver(ai1, ai2):
        newAI = ai.AI(
            ai1.fitness * ai1.heightWeight + ai2.fitness * ai2.heightWeight,
            ai1.fitness * ai1.linesWeight + ai2.fitness * ai2.linesWeight,
            ai1.fitness * ai1.holesWeight + ai2.fitness * ai2.holesWeight,
            ai1.fitness * ai1.bumpinessWeight + ai2.fitness * ai2.bumpinessWeight
        )
        trainingAlgorithm.normalize(newAI)
        return newAI
    
    def mutate(ai):
        mutate = random.random()*.4-0.2
        randomNum = random.randomint(0,3)
        if randomNum == 0:
            ai.heightWeight += mutate
        elif randomNum == 1:
            ai.linesWeight += mutate
        elif randomNum == 2:
            ai.holesWeight += mutate
        else:
            ai.bumpinessWeight += mutate

    def deleteAndReplace(allAi, newAi):
        allAi[:len(allAi) - len(newAi)]
        allAi = np.append(allAi, newAi)
        trainingAlgorithm.sort(allAi)
        return allAi
    
    def training(population, rounds, maxMoves):
        allAi = np.array(trainingAlgorithm.generateNewAi() for i in range(len(population)))
        print("finish initial population")
        # computeFitness(allAi, rounds, maxMoves) #Patrick implements
        trainingAlgorithm.sort(allAi)

        newAi = np.array()
        for i in range(30):
            parents = trainingAlgorithm.tournamentSelect(allAi)
            print('fitnesses = ' + parents[0].fitness + ',' + parents[1].fitness)
            child = trainingAlgorithm.crossOver(parents[0], parents[1])
            if random.random() < 0.05:
                trainingAlgorithm.mutate(child)
            newAi.append(child)

        # computeFitness(allAi, rounds, maxMoves) #Patrick implements
        trainingAlgorithm.deleteAndReplace(allAi,newAi)
        totalFitness = 0
        for ai in allAi:
            totalFitness += ai.fitness
        print("Average Fitness: ", totalFitness/len(allAi))
        print("Best AI: ")
        pprint(vars(allAi[0]))
        