import math
import ai
import random
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
    

    
        