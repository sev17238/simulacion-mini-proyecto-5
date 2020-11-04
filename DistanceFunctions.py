###################################################
# Guatemala, noviembre del 2020
###################################################
# Modelacion y simulacion
# Alejandro Tejada 17584
# Diego Sevilla 17238
###################################################
# Modulo de funciones para calculos de distancia
###################################################
# Refs:
# https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html
# https://vpetro.io/fuzzylogic/fuzzy_mehaan_joy.html
# https://gist.github.com/ryangmolina/e1c87509b6919ac8aaf3eceb315d3e5e
# https://www.geeksforgeeks.org/horn-clauses-in-deductive-databases/
# http://aima.cs.berkeley.edu/python/logic.html 
# https://boxbase.org/entries/2018/oct/8/horn-clauses-imperative-ir/

######IMPORTS ZONE ---------------------------------------------------------------------------
import numpy as np
import random
import math
########IMPORTS ZONE --------------------------------------------------------------------------

########FUNCTIONS ZONE ------------------------------------------------------------------------ 
def turningAngle(robotPosition, ballPosition, robotAngleView):
    '''returns the angle to turn and the direction of that angle.'''
    xr, yr = robotPosition
    xp, yp = ballPosition
    dy = yp - yr
    dx = xp - xr

    angleDirection = math.atan2(dy, dx)
    distanceTurnRight = 0
    distanceTurnLeft = 0
    if angleDirection < 0: angleDirection = math.degrees(angleDirection + 2 * math.pi)
    else: angleDirection = math.degrees(angleDirection)

    clockwiseDirection = -1
    opp_clockwiseDirection = 1

    ### check turning right distance
    if  robotAngleView >= angleDirection: distanceTurnRight = robotAngleView - angleDirection
    else: distanceTurnRight = robotAngleView - (angleDirection - 360)
    ### check turning left distance
    if  angleDirection >= robotAngleView: distanceTurnLeft = angleDirection - robotAngleView
    else: distanceTurnLeft = angleDirection - (robotAngleView - 360)
    ### returns y angle
    if distanceTurnRight <= distanceTurnLeft: return distanceTurnRight, clockwiseDirection
    else: return distanceTurnLeft, opp_clockwiseDirection

def distanceBetweenPoints(p1, p2):
    '''returns distance between 2 points'''
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def distanceToMoveXY(distance, angle):
    '''returns x and y coordinates to guide robot's destiny'''
    x = distance * math.cos(math.radians(angle))
    y = distance * math.sin(math.radians(angle))
    return x, y

def shootAngleDistance(robotPosition, goalPosition):
    '''returns angle for goal success'''
    xr, yr = robotPosition
    xp, yp = goalPosition
    dy = yp - yr
    dx = xp - xr

    angleDirection = math.atan2(dy, dx)
    distanceTurnRight = 0
    distanceTurnLeft = 0
    if angleDirection < 0: angleDirection = math.degrees(angleDirection + 2 * math.pi)
    else: angleDirection = math.degrees(angleDirection)

    return angleDirection, abs(xr - xp)

def shootReturnsY(x, angulo):
    '''returns y point for goal targeting accretion'''
    return x * math.tan(math.radians(angulo))
