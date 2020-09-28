import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('.')
from Player import Player
from config import playerConfig
from types import SimpleNamespace

def showPredictedRatings(player):
    ageList, predictedRatingList = [], []
    for age in range(15, 40):
        ageList.append(age)
        predictedRating = player.calculateRating(age)
        predictedRatingList.append(predictedRating)
    ageArray = np.array(ageList)
    predictedRatingArray = np.array(predictedRatingList)
    x, y = ageArray, predictedRatingArray
    plt.plot(x, y)
    for xy in zip(x, y):
        plt.text(
            xy[0] - 0.5,
            xy[1],
            int(xy[1]),
            {
                'weight': 'bold',
                'size'  : 10,
            }
        )
    plt.title(
        'Predicted Ratings for {} over time'.format(player.name),
        fontdict = {
            'weight': 'bold'
        }
    )
    plt.xlabel('Age')
    plt.ylabel('Predicted Rating')
    plt.axvline(
        x[np.argmax(y)],
        color = 'lightgray',
        linestyle = '--'
    )
    plt.show()

def showSkillDistribution(player):
    frameSize = 2.5
    ### Calculate vertices
    skills = player.skillDistribution
    points = {}
    for i, (skill, value) in enumerate(skills.items()):
        angle = 2 / len(skills) * i * np.pi
        pointX = value * np.sin(angle)
        sidePointX = frameSize * np.sin(angle)
        pointY = value * np.cos(angle)
        sidePointY = frameSize * np.cos(angle)
        labelX = (value + 0.375) * np.sin(angle)
        labelY = (value + 0.375) * np.cos(angle)
        points[skill] = {'x': pointX, 'y': pointY}
        plt.plot((0, sidePointX), (0, sidePointY), color = 'red', linewidth = 0.25)
        plt.text(labelX, labelY, "{0}\n{1:.1%}".format(skill, value), horizontalalignment = 'center', verticalalignment = 'center', fontdict = {'size': 8})
    pointsList = list(points.values())
    pointsList.append(pointsList[0]) ### Duplicate first point as last point to complete the shape

    ### Add edges between vertices
    for i in range(len(pointsList) - 1):
        plt.plot(
            (pointsList[i]['x'], pointsList[i + 1]['x']),
            (pointsList[i]['y'], pointsList[i + 1]['y']),
            color = 'black'
        )
    
    ### Fill shape and add center point for reference
    xPoints = [point['x'] for point in pointsList]
    yPoints = [point['y'] for point in pointsList]
    plt.fill(xPoints, yPoints, color = 'lightgray') ### TODO: Different colours for different positions? Variable colour based on skills e.g. more red for offence, more blue for defence, darker for more control, lighter for more spark?

    ### Frame plot
    plt.plot((-frameSize, frameSize), (frameSize, frameSize), color = "lightgray")
    plt.plot((frameSize, frameSize), (-frameSize, frameSize), color = "lightgray")
    plt.plot((-frameSize, frameSize), (-frameSize, -frameSize), color = "lightgray")
    plt.plot((-frameSize, -frameSize), (-frameSize, frameSize), color = "lightgray")

    ### Miscellaneous config
    bestPositionText = player.config['positions'][player.bestPosition]['realName']
    bestPositionText = bestPositionText.replace(' ', '\n')
    plt.text(0, 0, bestPositionText, horizontalalignment = 'center', verticalalignment = 'center', fontdict = {'size': 10, 'weight': 'bold'})
    plt.axis('off')
    plt.xlim(-frameSize, frameSize)
    plt.ylim(-frameSize, frameSize)
    plt.title(
        'Skill distribution for {}'.format(player.name),
        fontdict = {
            'weight': 'bold'
        }
    )

    ### Show plot
    plt.show()