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
from PIL import ImageGrab

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


def simulation(graph): 
    fieldLength = 180
    fieldWidth = 120

    robotInitialPosition = (random.randint(0,fieldLength),random.randint(0,fieldWidth))

    print("robot-initial-position: x:"+str(robotInitialPosition[0])+" y:"+str(robotInitialPosition[1]))
    
    #### Initial draws for robot and ball
    graph.draw_point((robotInitialPosition[0],robotInitialPosition[1]), size=12,color='blue')
    ballInitialPosition = (random.randint(0,fieldLength),random.randint(0,fieldWidth))
    robotInitialDirection = random.randint(0,359)
    graph.draw_point((ballInitialPosition[0],ballInitialPosition[1]), size=8,color='red')

    print()
    print("robot-initial-position: "+str(robotInitialPosition) + " robot-initial-direction:"+str(robotInitialDirection))
    print("ball-initial-position: "+str(ballInitialPosition))

    goalWidth = 12
    goalInitialPosition = (180, 50)

    ## UI FOR GOAL
    endGoal = (goalInitialPosition[0],goalInitialPosition[1]+12)
    graph.draw_line(goalInitialPosition,endGoal,color='green',width=4)

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

        ##robot UI
        graph.draw_point((robotInitialPosition[0],robotInitialPosition[1]), size=4,color='blue')
        ########################################### 


        if  currentDistance <= 9:
            print()
            print("it's time to shoot...!!")
            robotInitialPosition = ballInitialPosition
            robotInitialDirection, shootXDistance = shootAngleDistance(robotInitialPosition, goalInitialPosition)
            robotInitialDirection = robotInitialDirection + np.random.normal(0,5) ### deviation
            ballMovement = shootReturnsY(shootXDistance, robotInitialDirection) ### y ball position

            
            ### ball final position
            if (ballInitialPosition[1] +  ballMovement) > fieldWidth: 
                ballInitialPosition = (180, fieldWidth)
            elif (ballInitialPosition[1] +  ballMovement) < 0: 
                ballInitialPosition = (180, 0)
            else: 
                ballInitialPosition = (180, ballInitialPosition[1] +  ballMovement)
                ###UI FOR SHOOT
                graph.draw_line(robotInitialPosition,ballInitialPosition,color='yellow',width=2)

            print()
            print("current-position: "+str(robotInitialPosition))
            print("ball-initial-position: "+ str(ballInitialPosition))

            ### draw final position of ball
            graph.draw_point((ballInitialPosition[0],ballInitialPosition[1]), size=6,color='red')
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



####### UI --------------------------------------------------------------------------------------------


"""
    Demo - Drawing and moving demo
    This demo shows how to use a Graph Element to (optionally) display an image and then use the
    mouse to "drag" and draw rectangles and circles.
"""

def save_element_as_file(element, filename):
    """
    Saves any element as an image file.  Element needs to have an underlyiong Widget available (almost if not all of them do)
    :param element: The element to save
    :param filename: The filename to save to. The extension of the filename determines the format (jpg, png, gif, ?)
    """
    widget = element.Widget
    box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height())
    grab = ImageGrab.grab(bbox=box)
    grab.save(filename)



def main():

    sg.theme('Dark Blue 3')

    col = [[sg.T('Choose "Draw Points" and touch the canvas (click). \n After the simulation, erase the draw \nand give it another try.', enable_events=True)],
           [sg.R('Draw Rectangles', 1, key='-RECT-', enable_events=True)],
           [sg.R('Draw Circle', 1, key='-CIRCLE-', enable_events=True)],
           [sg.R('Draw Line', 1, key='-LINE-', enable_events=True)],
           [sg.R('Draw points', 1,  key='-POINT-', enable_events=True)],
           [sg.R('Erase item', 1, key='-ERASE-', enable_events=True)],
           [sg.R('Erase all', 1, key='-CLEAR-', enable_events=True)],
           [sg.R('Send to back', 1, key='-BACK-', enable_events=True)],
           [sg.R('Bring to front', 1, key='-FRONT-', enable_events=True)],
           [sg.R('Move Everything', 1, key='-MOVEALL-', enable_events=True)],
           [sg.R('Move Stuff', 1, True, key='-MOVE-', enable_events=True)],
           [sg.B('Save Image', key='-SAVE-')],
           ]

    layout = [[sg.Graph(
                canvas_size=(200, 150),
                graph_bottom_left=(0, 0),
                graph_top_right=(200, 150),
                key="-GRAPH-",
                enable_events=True,
                background_color='lightblue',
                drag_submits=True), sg.Col(col) ],
            [sg.Text(key='info', size=(60, 1))]]

    window = sg.Window("Drawing and Moving Stuff Around", layout, finalize=True)

    # get the graph element for ease of use later
    graph = window["-GRAPH-"]  # type: sg.Graph

    dragging = False
    start_point = end_point = prior_rect = None
    graph.bind('<Button-3>', '+RIGHT+')
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break  # exit
        if event in ('-MOVE-', '-MOVEALL-'):
            graph.Widget.config(cursor='fleur')
            # graph.set_cursor(cursor='fleur')          # not yet released method... coming soon!
        elif not event.startswith('-GRAPH-'):
            # graph.set_cursor(cursor='left_ptr')       # not yet released method... coming soon!
            graph.Widget.config(cursor='left_ptr')

        if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse
            x, y = values["-GRAPH-"]
            if not dragging:
                start_point = (x, y)
                dragging = True
                drag_figures = graph.get_figures_at_location((x,y))
                lastxy = x, y
            else:
                end_point = (x, y)
            if prior_rect:
                graph.delete_figure(prior_rect)
            delta_x, delta_y = x - lastxy[0], y - lastxy[1]
            lastxy = x,y
            if None not in (start_point, end_point):
                if values['-MOVE-']:
                    for fig in drag_figures:
                        graph.move_figure(fig, delta_x, delta_y)
                        graph.update()
                elif values['-RECT-']:
                    prior_rect = graph.draw_rectangle(start_point, end_point,fill_color='green', line_color='red')
                elif values['-CIRCLE-']:
                    prior_rect = graph.draw_circle(start_point, end_point[0]-start_point[0], fill_color='red', line_color='green')
                elif values['-LINE-']:
                    prior_rect = graph.draw_line(start_point, end_point, width=4)
                elif values['-POINT-']:
                    #graph.draw_point((x,y), size=8,color='blue')
                    simulation(graph)
                elif values['-ERASE-']:
                    for figure in drag_figures:
                        graph.delete_figure(figure)
                elif values['-CLEAR-']:
                    graph.erase()
                elif values['-MOVEALL-']:
                    graph.move(delta_x, delta_y)

        elif event.endswith('+UP'):  # The drawing has ended because mouse up
            info = window["info"]
            info.update(value=f"grabbed rectangle from {start_point} to {end_point}")
            start_point, end_point = None, None  # enable grabbing a new rect
            dragging = False
            prior_rect = None
        elif event == '-SAVE-':
            # filename = sg.popup_get_file('Choose file (PNG, JPG, GIF) to save to', save_as=True)
            filename=r'simulation_test.jpg'
            save_element_as_file(window['-GRAPH-'], filename)

    window.close()

##### UI ----------------------------------------------------------------------------------------------

main()
