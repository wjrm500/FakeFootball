from scipy import spatial, stats
from config import playerConfig
import numpy as np

positionPoints = {}
for key, value in playerConfig['positions'].items():
    positionPoints[key] = list(value['skillDistribution'].values())

positionDistances = {}
for position, point in positionPoints.items():
    positionDistances[position] = {}
    for position2, point2 in positionPoints.items():
        if position != position2:
            positionDistances[position][position2] = spatial.distance.cosine(point, point2)

positionDistanceMeans = {}
for position, distances in positionDistances.items():
    positionDistanceMeans[position] = np.mean(list(distances.values()))

mu = playerConfig['skill']['distribution']['mean']
sigma = playerConfig['skill']['distribution']['stDev']

positionPointsProbabilities = {}
for position, points in positionPoints.items():
    pointsProbability = 1
    for point in points:
        pointsProbability *= stats.norm(mu, sigma).cdf(point)
    positionPointsProbabilities[position] = pointsProbability

positionLikelihoodEstimates = {}
for position in positionDistanceMeans.keys():
    meanDistance = positionDistanceMeans[position]
    probability = positionPointsProbabilities[position]
    likelihoodEstimate = meanDistance * probability
    positionLikelihoodEstimates[position] = likelihoodEstimate

updatedPositionLikelihoodEstimates = {}
for position, likelihoodEstimate in positionLikelihoodEstimates.items():
    updatedPositionLikelihoodEstimates[position] = likelihoodEstimate * 1 / np.sum(list(positionLikelihoodEstimates.values()))

for key, value in updatedPositionLikelihoodEstimates.items():
    print(key, ": ", round(value, 2))