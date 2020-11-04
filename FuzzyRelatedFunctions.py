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
# http://aima.cs.berkeley.edu/python/logic.html 


######IMPORTS ZONE ---------------------------------------------------------------------------
import numpy as np
import random
import math
########IMPORTS ZONE --------------------------------------------------------------------------

########FUNCTIONS ZONE ------------------------------------------------------------------------ 
def trimf(x, points):
    pointA = points[0]
    pointB = points[1]
    pointC = points[2]
    slopeAB = getSlope(pointA, 0, pointB, 1)
    slopeBC = getSlope(pointB, 1, pointC, 0)
    result = 0
    if x >= pointA and x <= pointB:
        result = slopeAB * x + getYIntercept(pointA, 0, pointB, 1)
    elif x >= pointB and x <= pointC:
        result = slopeBC * x + getYIntercept(pointB, 1, pointC, 0)
    return result

def trapmf(x, points):
    pointA = points[0]
    pointB = points[1]
    pointC = points[2]
    pointD = points[3]
    slopeAB = getSlope(pointA, 0, pointB, 1)
    slopeCD = getSlope(pointC, 1, pointD, 0)
    yInterceptAB = getYIntercept(pointA, 0, pointB, 1)
    yInterceptCD = getYIntercept(pointC, 1, pointD, 0)
    result = 0
    if x > pointA and x < pointB:
        result = slopeAB * x + yInterceptAB
    elif x >= pointB and x <= pointC:
        result = 1
    elif x > pointC and x < pointD:
        result = slopeCD * x + yInterceptCD
    return result

def getSlope(x1, y1, x2, y2):
    # Avoid zero division error of vertical line for shouldered trapmf
    try:
        slope = (y2 - y1) / (x2 - x1)
    except ZeroDivisionError:
        slope = 0
    return slope

def getYIntercept(x1, y1, x2, y2):
    m = getSlope(x1, y1, x2, y2)
    if y1 < y2:
        y = y2
        x = x2
    else:
        y = y1
        x = x1
    return y - m * x

def getTrimfPlots(start, end, points):
    plots = [0] * (abs(start) + abs(end))
    pointA = points[0]
    pointB = points[1]
    pointC = points[2]
    slopeAB = getSlope(pointA, 0, pointB, 1)
    slopeBC = getSlope(pointB, 1, pointC, 0)
    yInterceptAB = getYIntercept(pointA, 0, pointB, 1)
    yInterceptBC = getYIntercept(pointB, 1, pointC, 0)
    for i in range(pointA, pointB):
        plots[i] = slopeAB * i + yInterceptAB
    for i in range(pointB, pointC):
        plots[i] = slopeBC * i + yInterceptBC

    return plots

def getTrapmfPlots(start, end, points, shoulder=None):
    plots = [0] * (abs(start) + abs(end))
    pointA = points[0]
    pointB = points[1]
    pointC = points[2]
    pointD = points[3]
    left = 0
    right = 0
    slopeAB = getSlope(pointA, 0, pointB, 1)
    slopeCD = getSlope(pointC, 1, pointD, 0)
    yInterceptAB = getYIntercept(pointA, 0, pointB, 1)
    yInterceptCD = getYIntercept(pointC, 1, pointD, 0)
    if shoulder == "left":
        for i in range(start, pointA):
            plots[i] = 1
    elif shoulder == "right":
        for i in range(pointD, end):
            plots[i] = 1
    for i in range(pointA, pointB):
        plots[i] = slopeAB * i + yInterceptAB
    for i in range(pointB, pointC):
        plots[i] = 1
    for i in range(pointC, pointD):
        plots[i] = slopeCD * i + yInterceptCD
    return plots

def getCentroid(aggregatedPlots):
    '''centroid related, returns de centroid of the current plot'''
    n = len(aggregatedPlots)
    xAxis = list(range(n))
    centroidNum = 0
    centroidDenum = 0
    for i in range(n):
        centroidNum += xAxis[i] * aggregatedPlots[i]
        centroidDenum += aggregatedPlots[i]
    return centroidNum / centroidDenum


def generator2DFunctions(points):
    '''This function returns an inner function that receives 4 points as params to 
    determine the function's shape.'''

    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    x4, y4 = points[3]
    ### first road
    m1 = (y2 * 1.0 - y1 * 1.0) / (x2 * 1.0 - x1 * 1.0)
    b1 = y2 - m1 * x2
    ### second 
    m2 = (y3 * 1.0 - y2 * 1.0) / (x3 * 1.0 - x2 * 1.0)
    b2 = y3 - m2 * x3
    ### third
    m3 = (y4 * 1.0 - y3 * 1.0) / (x4 * 1.0 - x3 * 1.0)
    b3 = y4 - m3 * x4

    def inner2DFunction(d):
        if d > x3:
            res = d * m3 + b3
            return res
        elif d > x2:
            res = d * m2 + b2
            return res
        else:
            res = d * m1 + b1
            return res

    return inner2DFunction


### HORN Clauses
# https://www.geeksforgeeks.org/horn-clauses-in-deductive-databases/
# https://boxbase.org/entries/2018/oct/8/horn-clauses-imperative-ir/
def hornAND(fa1, fa2, fc3):
    def innerHornAND(ds,rs,es): return min(min(fa1(ds), fa2(ds)), fc3(es))
    return innerHornAND
def hornOR(fa1, fa2, fc3):
    def innerHornOR(ds,rs,es): return min(max(fa1(ds), fa2(rs)), fc3(es))
    return innerHornOR

### Points for input crisp functions
youAreCloserPoints = [(0,1),(10,1),(170,0),(180,0)]
youAreFurtherAwayPoints = [(0,0),(10,0),(170,1),(180,1)]
directTargetingPoints = [(0,1),(20,1),(140,0),(160,0)]
oppositeTargetingPoints = [(0,0),(20,0),(140,1),(160,1)]

### Points for output crisp functions
turnALittlePoints = [(0,1),(3,1),(7,0),(10,0)]
turnALotPoints = [(0,0),(3,0),(7,1),(10,1)]
moveALittlePoints = [(0,1),(2,1),(4,0),(5,0)]
moveALotPoints = [(0,0),(2,0),(4,1),(5,1)]

moveALittle = generator2DFunctions(moveALittlePoints) ### output crisp distance fucntions
moveALot = generator2DFunctions(moveALotPoints)
turnALittle = generator2DFunctions(turnALittlePoints) ### output crisp rotation functions
turnALot = generator2DFunctions(turnALotPoints)
itsPointingDirectly = generator2DFunctions(directTargetingPoints) ### input crisp rotation functions
itsPointingOppositeSide = generator2DFunctions(oppositeTargetingPoints)
itsCloser =  generator2DFunctions(youAreCloserPoints) ### input crisp distance functions
itsFurtherAway = generator2DFunctions(youAreFurtherAwayPoints)

### Horn distance clauses 
hornD1 = hornOR(itsCloser, itsPointingOppositeSide, moveALittle) ### if close or viewing opp, move a little
hornD2 = hornOR(itsFurtherAway, itsPointingDirectly, moveALot) ### if away or viewing directly, move a lot
### horn rotation clauses
hornR1 = hornOR(itsFurtherAway, itsPointingOppositeSide, turnALot) ##if away or view opp, rotate a lot
hornR2 = hornOR(itsCloser, itsPointingDirectly, turnALittle) ##if close or view directly, rotate a little

fuzzyDistanceOutput = lambda ds, rs, es : max( ### fuzzy output for distance
    hornD1(ds,rs,es),
    hornD2(ds,rs,es)
)
fuzzyRotationOutput = lambda ds, rs, es : max( ### fuzzy output for rotation
    hornR1(ds,rs,es),
    hornR2(ds,rs,es)
)

def fuzzyDistance(ballMovement, ballRotation):
    '''returns fuzzy distance to travel'''
    xs = np.linspace(0, 5, 120)
    ys = [fuzzyDistanceOutput(ballMovement, ballRotation, x) for x in xs]
    return np.sum(xs * ys) / np.sum(ys) 

def fuzzyRotation(ballMovement, ballRotation):
    '''returns fuzzy rotation to execute'''
    xs = np.linspace(0, 10, 120)
    ys = [fuzzyDistanceOutput(ballMovement, ballRotation, x) for x in xs]
    return np.sum(xs * ys) / np.sum(ys) 
