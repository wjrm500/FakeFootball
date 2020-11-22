import pickle
from Club import Club
from Manager import Manager
from Player import Player
import numpy as np
import copy
import Utils

with open('LinearRegression21948', 'rb') as file:
    model = pickle.load(file)

data = []
for i in range(10_000):
    print(i)
    club = Club(Manager(), [Player() for i in range(40)])
    x1 = np.array([list(club.features.values())])
    rankBefore = model.predict(x1)
    clubRating = club.features['strength']

    prospectivePlayer = Player()
    playerAge, playerRating = prospectivePlayer.age, prospectivePlayer.rating

    futureRanks = {}
    for yearsIntoFuture in range(1, 11):
        clubCopy = copy.deepcopy(club)
        futureVersion = prospectivePlayer.getFutureVersion(yearsIntoFuture)
        clubCopy.addFutureVersion(futureVersion)
        clubCopy.conductInitialAppraisal()
        clubCopy.setFeatures()
        x2 = np.array([list(clubCopy.features.values())])
        futureRanks[yearsIntoFuture] = model.predict(x2)

    # print('Club rating: {} - Player age: {} - Player rating: {}'.format(
    #     round(clubRating, 2),
    #     prospectivePlayer.age,
    #     round(playerRating, 2)
    #     )
    # )
    predictedRankWithoutPlayer = Utils.limitValue(rankBefore[0], mn = 1, mx = 20)
    # print('Predicted rank without player: {}'.format(round(predictedRankWithoutPlayer, 2)))
    totalValueAdded = 0
    for yearsIntoFuture, rank in futureRanks.items():
        predictedRankWithPlayer = Utils.limitValue(rank[0], mn = 1, mx = 20)
        predictedRankValues = list(map(lambda x: 1 - (np.power(x, (1 / 5)) / 2) * 100_000_000, [predictedRankWithoutPlayer, predictedRankWithPlayer]))
        valueAdded = Utils.limitValue(predictedRankValues[1] - predictedRankValues[0], mn = 0)
        valueAddedWithFutureTax = valueAdded * (1 - (np.power(yearsIntoFuture, (1 / 5)) / 2)) * 2
        totalValueAdded += valueAddedWithFutureTax
        # print('Year {:2} - Predicted rank: {:.2f} - Value added: {:8} - Value added with future tax: {:8}'.format(
        #     yearsIntoFuture,
        #     round(predictedRankWithPlayer, 2),
        #     '£{:,}'.format(int(valueAdded)),
        #     '£{:,}'.format(int(valueAddedWithFutureTax))
        #     )
        # )
    # print('Total value added: £{:,}'.format(int(totalValueAdded)))
    # print('\r')
    data.append(','.join(map(str, [clubRating, predictedRankWithoutPlayer, playerAge, playerRating, totalValueAdded])))

with open('transferValues.txt', 'w') as file:
    for item in data:
        file.write(item)
        file.write('\n')
### Clubs who are finishing below their expected finishing positions could prioritise short term value (increase future tax)