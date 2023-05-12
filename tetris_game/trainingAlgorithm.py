import math
import ai
import trainingGame
import random
import numpy as np
from pprint import pprint


class trainingAlgorithm:
    def normalize(ai):

        norm = math.sqrt(ai.heightWeight**2 + ai.linesWeight **
                         2 + ai.holesWeight**2 + ai.bumpinessWeight**2)
        ai.heightWeight /= norm
        ai.linesWeight /= norm
        ai.holesWeight /= norm
        ai.bumpinessWeight /= norm

    def generateNewAi():
        newAI = ai.AI(random.random()*2-1,
                      random.random()*2-1,
                      random.random()*2-1,
                      random.random()*2-1)
        trainingAlgorithm.normalize(newAI)
        return newAI

    def generateOldAi():
        oldAi = ai.AI(-0.550640755084,
                      0.301200234921,
                      -0.724338713385,
                      -0.285318428453)
        trainingAlgorithm.normalize(oldAi)
        return oldAi

    def sort(allAi):
        return sorted(allAi, key=lambda ai: ai.fitness, reverse=True)

    def tournamentSelect(allAi):
        indices = np.random.choice(len(allAi)-1, len(allAi)//3, replace=False)

        indices = np.sort(indices)
        return [allAi[indices[0]], allAi[indices[1]]]

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
        mutate = random.random()*.7-0.7
        randomNum = random.randint(0, 3)
        if randomNum == 0:
            ai.heightWeight += mutate
        elif randomNum == 1:
            ai.linesWeight += mutate
        elif randomNum == 2:
            ai.holesWeight += mutate
        else:
            ai.bumpinessWeight += mutate

    def deleteAndReplace(allAi, newAi):

        allAi = allAi[:len(allAi) - len(newAi)]
        allAi = np.append(allAi, newAi)
        allAi = trainingAlgorithm.sort(allAi)
        return allAi

    def training(population, rounds, maxMoves):
        allAi = []
        for i in range(population-1):
            allAi.append(trainingAlgorithm.generateNewAi())

        # ADD PREVIOUS OPTIMAL TO SHORTCUT SLOW INITIAL TRAINING
        allAi.append(trainingAlgorithm.generateOldAi())

        trainingGame.computeFitness(
            allAi, rounds, maxMoves)  # Patrick implements
        allAi = trainingAlgorithm.sort(allAi)

        iter = 1
        while True:
            newAi = []
            for i in range(population//3):

                parents = trainingAlgorithm.tournamentSelect(allAi)
                # print('fitnesses = ' +
                #   str(parents[0].fitness) + ',' + str(parents[1].fitness))

                child = trainingAlgorithm.crossOver(parents[0], parents[1])
                if random.random() < .5:
                    trainingAlgorithm.mutate(child)
                newAi.append(child)

            trainingGame.computeFitness(
                newAi, rounds, maxMoves)  # Patrick implements
            allAi = trainingAlgorithm.deleteAndReplace(allAi, newAi)
            allAi = trainingAlgorithm.sort(allAi)
            totalFitness = 0
            for ai in allAi:
                totalFitness += ai.fitness
            print("Iteration: ", iter)
            print("Average Fitness: ", totalFitness/len(allAi))
            print("Best AI: ")
            pprint(vars(allAi[0]))
            iter += 1


trainingAlgorithm.training(50, 1, 5000)
