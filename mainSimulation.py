###################################################
# Guatemala, noviembre del 2020
###################################################
# Modelacion y simulacion
# Alejandro Tejada 17584
# Diego Sevilla 17238
###################################################
# Programa principal
###################################################
# Refs:
# https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html
# https://vpetro.io/fuzzylogic/fuzzy_mehaan_joy.html
# https://gist.github.com/ryangmolina/e1c87509b6919ac8aaf3eceb315d3e5e
# http://aima.cs.berkeley.edu/python/logic.html 


######IMPORTS ZONE ---------------------------------------------------------------------------
import numpy as np
import random
import math
import PySimpleGUI as sg

from FuzzyRelatedFunctions import *
from DistanceFunctions import *
########IMPORTS ZONE --------------------------------------------------------------------------


######FUNCTIONS ZONE --------------------------------------------------------------------------
def evaluateRules(error, errorDerivative):
    rules = [[0] * 3 for i in range(3)]

    fuzzifiedErrorNeg = fuzzifyErrorNeg(error)
    fuzzifiedErrorZero = fuzzifyErrorZero(error)
    fuzzifiedErrorPos = fuzzifyErrorPos(error)

    fuzzifiedErrorDotNeg = fuzzifyErrorDotNeg(errorDerivative)
    fuzzifiedErrorDotZero = fuzzifyErrorDotZero(errorDerivative)
    fuzzifiedErrorDotPos = fuzzifyErrorDotPos(errorDerivative)
    # RULE 1
    rules[0][0] = min(fuzzifiedErrorNeg, fuzzifiedErrorDotNeg)
    # RULE 2
    rules[0][1] = min(fuzzifiedErrorZero, fuzzifiedErrorDotNeg)
    # RULE 3
    rules[0][2] = min(fuzzifiedErrorPos, fuzzifiedErrorDotNeg)
    # RULE 4
    rules[1][0] = min(fuzzifiedErrorNeg, fuzzifiedErrorDotZero)
    # RULE 5
    rules[1][1] = min(fuzzifiedErrorZero, fuzzifiedErrorDotZero)
    # RULE 6
    rules[1][2] = min(fuzzifiedErrorPos, fuzzifiedErrorDotZero)
    # RULE 7
    rules[2][0] = min(fuzzifiedErrorNeg, fuzzifiedErrorDotPos)
    # RULE 8
    rules[2][1] = min(fuzzifiedErrorZero, fuzzifiedErrorDotPos)
    # RULE 9
    rules[2][2] = min(fuzzifiedErrorPos, fuzzifiedErrorDotPos)
    return rules


def fuzzifyErrorPos(error):
    return trimf(error, [0, 5, 5])


def fuzzifyErrorZero(error):
    return trimf(error, [-5, 0, 5])


def fuzzifyErrorNeg(error):
    return trimf(error, [-5, -5, 0])


def fuzzifyErrorDotPos(errorDot):
    return trapmf(errorDot, [1, 1.5, 5, 5])


def fuzzifyErrorDotZero(errorDot):
    return trimf(errorDot, [-2, 0, 2])


def fuzzifyErrorDotNeg(errorDot):
    return trapmf(errorDot, [-5, -5, -1.5, -1])


def fuzzifyOutputCooler():
    return getTrapmfPlots(0, 200, [0, 0, 30, 95], "left")


def fuzzifyOutputNoChange():
    return getTrimfPlots(0, 200, [90, 100, 110])


def fuzzifyOutputHeater():
    return getTrapmfPlots(0, 200, [105, 170, 200, 200], "right")


def fisAggregation(rules, pcc, pcnc, pch):
    result = [0] * 200
    for rule in range(len(rules)):
        for i in range(200):
            if rules[rule][0] > 0 and i < 95:
                result[i] = min(rules[rule][0], pcc[i])
            if rules[rule][1] > 0 and i > 90 and i < 110:
                result[i] = min(rules[rule][1], pcnc[i])
            if rules[rule][2] > 0 and i > 105 and i < 200:
                result[i] = min(rules[rule][2], pch[i])
    return result
######FUNCTIONS ZONE --------------------------------------------------------------------------


fieldLength = 180
fieldWidth = 120

robotInitialPosition = (random.randint(0,fieldLength),random.randint(0,fieldWidth))
ballInitialPosition = (random.randint(0,fieldLength),random.randint(0,fieldWidth))
robotInitialDirection = random.randint(0,359)
print()
print("robot-initial-position: "+str(robotInitialPosition) + " robot-initial-direction:"+str(robotInitialDirection))
print("ball-initial-position: "+str(ballInitialPosition))

goalWidth = 12
goalInitialPosition = (180, 50)
print("goal-width: "+str(goalWidth))
print("goal-initial-position: "+str(goalInitialPosition))

currentDistance = distanceBetweenPoints(robotInitialPosition, ballInitialPosition)
print("current-initial-distance: "+str(currentDistance))

print("---------------------------------")
print()

goool = False

while (not goool) or (currentDistance > 9):

    distanceToTravel = distanceBetweenPoints(robotInitialPosition, ballInitialPosition)
    rotationAngle, angleDirection = turningAngle(robotInitialPosition, ballInitialPosition, robotInitialDirection)
    print()
    print("inputs")
    print("distance-to-travel: "+str(distanceToTravel))
    print("rotation-angle: "+str(rotationAngle) + " angle-direction: "+str(angleDirection))

    distance = fuzzyDistance(distanceToTravel, rotationAngle)
    rotation = fuzzyRotation(distanceToTravel, rotationAngle)
    print("Fuzzy results")
    print("distance: "+str(distance))
    print("rotation: "+str(rotation))

    finalXPosition = 0
    finalYPosition = 0

    x, y = distanceToMoveXY(distance, ((robotInitialDirection + angleDirection * rotation) % 360))
    currentRobotXPosition, currentRobotYPosition = robotInitialPosition
    print("Update x, y position coordinates: ")
    print("x:"+str(x)+" y:"+str(y))

    if (x + currentRobotXPosition) > fieldLength: finalXPosition = fieldLength
    elif (x + currentRobotXPosition) < 0: finalXPosition = 0
    else: finalXPosition = x + currentRobotXPosition

    if (y + currentRobotYPosition) > fieldWidth: finalYPosition = fieldWidth
    elif (y + currentRobotYPosition) < 0: finalYPosition = 0
    else: finalYPosition = y + currentRobotYPosition

    ### update position and rotation
    robotInitialPosition = (finalXPosition, finalYPosition)
    robotInitialDirection = (robotInitialDirection + angleDirection * rotation) % 360
    currentDistance = distanceBetweenPoints(robotInitialPosition, ballInitialPosition) ### check

    print("current-position: "+str(robotInitialPosition))
    print("robot-initial-direction: "+str(robotInitialDirection))
    print("current-distance: "+str(currentDistance))

    ###########################################


    if  currentDistance <= 9:
        print()
        print("it's time to shoot...!!")
        robotInitialPosition = ballInitialPosition
        robotInitialDirection, shootXDistance = shootAngleDistance(robotInitialPosition, goalInitialPosition)
        robotInitialDirection = robotInitialDirection + np.random.normal(0,5) ### deviation
        ballMovement = shootReturnsY(shootXDistance, robotInitialDirection) ### y ball position

        ### ball final position
        if (ballInitialPosition[1] +  ballMovement) > fieldWidth: ballInitialPosition = (180, fieldWidth)
        elif (ballInitialPosition[1] +  ballMovement) < 0: ballInitialPosition = (180, 0)
        else: ballInitialPosition = (180, ballInitialPosition[1] +  ballMovement)

        print()
        print("current-position: "+str(robotInitialPosition))
        print("ball-initial-position: "+ str(ballInitialPosition))

        #############################################

        ### if gol, end simulation
        if (ballInitialPosition[1] > (goalInitialPosition[1] - goalWidth)) and (ballInitialPosition[1] < (goalInitialPosition[1] + goalWidth)):
            print()
            print('Goool!')
            print('3 cheers for Robby!')
            print('horray! ...Horray! ...HORRAY!')
            print()
            goool = True
        else:
            print('Fail! The ball is out the goal.')
            ##randomize values
            robotInitialPosition = (random.randint(0,fieldLength),
            random.randint(0,fieldWidth))
            ballInitialPosition = (random.randint(0,fieldLength),
            random.randint(0,fieldWidth))
            robotInitialDirection = random.randint(0,359)
            currentDistance = distanceBetweenPoints(robotInitialPosition, 
            ballInitialPosition)

            print(str(robotInitialPosition))
            print(str(ballInitialPosition))
            print(str(robotInitialDirection))
            print(str(currentDistance))

            ##########################################

print("Simulation Over")
