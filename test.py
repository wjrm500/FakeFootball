from Player import Player
from config import playerConfig
from types import SimpleNamespace
from Utilities.PlayerUtils import showSkillDistribution

positionInstances = []
ageInstances = []
numPlayers = 10_000
for i in range(numPlayers):
    player = Player(playerConfig)
    if player.retired == False:
        positionInstances.append(player.bestPosition)
    else:
        ageInstances.append(player.age)
    # print(player.bestPosition, {key: round(value, 2) for key, value in player.skillDistribution.items()})

actual = {position: positionInstances.count(position) for position in set(positionInstances)}
### targets taken from https://blog.wyscout.com/most-used-formations-europe/
target = {'CF': 0.135, 'WF': 0.066, 'CAM': 0.055, 'WM': 0.101, 'CM': 0.125, 'CDM': 0.094, 'WB': 0.048, 'FB': 0.152, 'CB': 0.224}
numActivePlayers = len(positionInstances)
print(actual)
print("Number of active players: ", numActivePlayers)
d = {position: {'actual': round(actual[position] / numActivePlayers, 3), 'target': target[position]} for position in target.keys()}
for key, value in d.items():
    print(key, value)
# ageDict = {"'" + str(age) + "'": ageInstances.count(age) for age in set(ageInstances)}
# for key, value in ageDict.items():
#     print(key, value)

# player = Player(playerConfig)
# from pprint import pprint
# pprint(vars(player))
# showSkillDistribution(player)