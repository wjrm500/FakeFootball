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
    ### TODO: Create generic RadarChart function in a GraphUtils file, capable of generating a radar chart from any set of items

    ### Turn items in a player's skill distribution dictionary into local variables
    n = SimpleNamespace(**player.skillDistribution)

    ### Calculate vertices
    points = {
        'offence': {'x': 0         , 'y': n.offence },
        'spark'  : {'x': n.spark   , 'y': 0         },
        'defence': {'x': 0         , 'y': -n.defence},
        'control': {'x': -n.control, 'y': 0         }
    } 
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
    
    ### Add labels
    plt.text(0, n.offence + 0.3, "{0:.0%}".format(n.offence), horizontalalignment = 'center')
    plt.text(0, n.offence + 0.1, 'Offence', horizontalalignment = 'center')
    plt.text(n.spark + 0.1, 0.05, "{0:.0%}".format(n.spark), horizontalalignment = 'left')
    plt.text(n.spark + 0.1, -0.15, 'Spark', horizontalalignment = 'left')
    plt.text(0, -n.defence - 0.25, "{0:.0%}".format(n.defence), horizontalalignment = 'center')
    plt.text(0, -n.defence - 0.45, 'Defence', horizontalalignment = 'center')
    plt.text(-n.control - 0.1, 0.05, "{0:.0%}".format(n.control), horizontalalignment = 'right')
    plt.text(-n.control - 0.1, -0.15, 'Control', horizontalalignment = 'right')

    ### Frame plot
    plt.plot((-2, 2), (2, 2), color = "lightgray")
    plt.plot((2, 2), (-2, 2), color = "lightgray")
    plt.plot((-2, 2), (-2, -2), color = "lightgray")
    plt.plot((-2, -2), (-2, 2), color = "lightgray")

    ### Miscellaneous config
    # plt.plot(0, 0, 'o', color = 'black')
    plt.text(0, 0, player.bestPosition, horizontalalignment = 'center')
    plt.axis('off')
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.title(
        'Skill distribution for {}'.format(player.name),
        fontdict = {
            'weight': 'bold'
        }
    )

    ### Show plot
    plt.show()