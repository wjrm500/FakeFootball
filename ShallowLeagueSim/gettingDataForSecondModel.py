import pickle
from Club import Club
from Manager import Manager
from Player import Player
import numpy as np
import copy
import Utils
from datetime import datetime

def inTopThreePositions(player, position):
    topThreePositions = list(map(lambda x: x[0], sorted(player.positionRatings.items(), key = lambda x: x[1])))[-3:]
    return position in topThreePositions

### LinearRegression43336 is the linear regression model used to predict rank

with open('LinearRegression43336', 'rb') as file:
    model = pickle.load(file)

data = []
print(datetime.now())
for i in range(10_000):
    print(i)
    dataItem = {'features': {}, 'labels': {}}
    club = Club(Manager())
    x1 = np.array([list(club.features.values())])
    predictedRankWithoutPlayer = model.predict(x1)
    predictedRankWithoutPlayer = Utils.limitValue(predictedRankWithoutPlayer[0], mn = 1, mx = 20)

    dataItem['features']['clubStrength'] = club.features['strength']
    dataItem['features']['clubDepth'] = club.features['depth']
    dataItem['features']['predictedRankWithoutPlayer'] = predictedRankWithoutPlayer

    prospectivePlayer = Player()
    predictedRanksWithPlayer = {}
    for yearsIntoFuture in range(1, 11):
        clubCopy = copy.deepcopy(club)
        futureVersion = prospectivePlayer.getFutureVersion(yearsIntoFuture)
        clubCopy.addFutureVersion(futureVersion)
        clubCopy.conductInitialAppraisal()
        clubCopy.setFeatures()
        x2 = np.array([list(clubCopy.features.values())])
        predictedRanksWithPlayer[yearsIntoFuture] = model.predict(x2)
    
    dataItem['features']['playerAge'] = prospectivePlayer.age
    dataItem['features']['playerRating'] = prospectivePlayer.rating
    dataItem['features']['playerPeakAge'] = prospectivePlayer.peakAge
    dataItem['features']['playerPeakRating'] = prospectivePlayer.peakRating

    for n in range(1, 4):
        ### Get nth best position of prospective player with corresponding position rating, where 1 <= n <= 3
        nthBestPositionRatingTuple = sorted(prospectivePlayer.positionRatings.items(), key = lambda x: x[1])[-n]
        nthBestPosition, nthBestPositionRating = nthBestPositionRatingTuple
    
        ### Get top three position ratings at club for prospective player's nth best position
        ratings = []
        for player in club.squad:
            for position, rating in player.positionRatings.items():
                if position == nthBestPosition and inTopThreePositions(player, position):
                    ratings.append(rating)
        ratings.sort()
        topThreeRatings = ratings[-3:]
        while len(topThreeRatings) < 3:
            topThreeRatings.insert(0, 0)

        ### Add features to dataItem
        dataItem['features']['position' + str(n) + 'PlayerRating'] = nthBestPositionRating
        for j in range(1, 4):
            dataItem['features']['position' + str(n) + 'ClubRating' + str(j)] = topThreeRatings[-j]

    # print('Club rating: {} - Predicted rank without player: {} - Player peak age: {} - Player age: {} - Player peak rating: {} -  Player rating: {}'.format(
    #     round(club.features['strength'], 2),
    #     round(predictedRankWithoutPlayer, 2),
    #     round(prospectivePlayer.age, 2),
    #     round(prospectivePlayer.peakRating, 2),
    #     round(prospectivePlayer.peakAge, 2),
    #     round(prospectivePlayer.rating, 2),
    #     )
    # )
    totalValueAdded = 0
    for yearsIntoFuture, predictedRankWithPlayer in predictedRanksWithPlayer.items():
        predictedRankWithPlayer = Utils.limitValue(predictedRankWithPlayer[0], mn = 1, mx = 20)
        predictedRankValues = list(map(lambda x: 1 - (np.power(x, (1 / 5)) / 2) * 100_000_000, [predictedRankWithoutPlayer, predictedRankWithPlayer]))
        valueAdded = Utils.limitValue(predictedRankValues[1] - predictedRankValues[0], mn = 0)
        valueAddedWithFutureTax = valueAdded * (1 - (np.power(yearsIntoFuture, (1 / 5)) / 2)) * 2
        totalValueAdded += valueAddedWithFutureTax

    #     ###
    #     print('Year {:2} - Predicted rank with player: {:.2f} - Value added: {:8} - Value added with future tax: {:8}'.format(
    #         yearsIntoFuture,
    #         round(predictedRankWithPlayer, 2),
    #         '£{:,}'.format(int(valueAdded)),
    #         '£{:,}'.format(int(valueAddedWithFutureTax))
    #         )
    #     )
    # print('Total value added: £{:,}'.format(int(totalValueAdded)))
    # print('\r')
    # ###

    dataItem['labels']['totalValueAdded'] = totalValueAdded
    data.append(dataItem)

Utils.pickleObject(data)

# with open('transferValues.txt', 'w') as file:
#     for item in data:
#         a = [str(val2) for val in item.values() for val2 in val.values()]
#         file.write(','.join(a))
#         file.write('\r')

print(datetime.now())
### Clubs who are finishing below their expected finishing positions could prioritise short term value (increase future tax)