from Player import Player
from types import SimpleNamespace
from Utilities.PlayerUtils import showSkillDistribution

#normalise to a position - once position found adjust stats in that direction

# positionInstances = []
# ageInstances = []
# numPlayers = 100_000
# for i in range(numPlayers):
#     player = Player(playerConfig)
#     if player.retired == False:
#         positionInstances.append(player.bestPosition)
#     else:
#         ageInstances.append(player.age)
#     # print(player.bestPosition, {key: round(value, 2) for key, value in player.skillDistribution.items()})

# actual = {position: positionInstances.count(position) for position in set(positionInstances)}
# ### targets taken from https://blog.wyscout.com/most-used-formations-europe/
# target = {'CF': 0.135, 'WF': 0.066, 'COM': 0.055, 'WM': 0.101, 'CM': 0.125, 'CDM': 0.094, 'WB': 0.048, 'FB': 0.152, 'CB': 0.224}
# numActivePlayers = len(positionInstances)
# print(actual)
# print("Number of active players: ", numActivePlayers)
# d = {position: {'actual': round(actual[position] / numActivePlayers, 3), 'target': target[position]} for position in target.keys()}
# for key, value in d.items():
#     print(key, value)
# # ageDict = {"'" + str(age) + "'": ageInstances.count(age) for age in set(ageInstances)}
# # for key, value in ageDict.items():
# #     print(key, value)

# player = Player(
#     config = {
#         'peakAge': {'mean': 27, 'stDev': 0},
#         'peakRating': {'mean': 99, 'stDev': 0}
#         },
#     age = 27
#     )
from pprint import pprint
players = []
while len(players) < 8:
    player = Player()
    if player.retired is False:
        players.append(player)
        # pprint(vars(player))


showSkillDistribution(players, projection = True, labels = True)
print('hello')