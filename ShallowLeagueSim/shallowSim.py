from League import League
from Club import Club
from Player import Player
from Manager import Manager
from Match import Match
import Utils
from datetime import datetime

print(datetime.now())

data = []
for i in range(1_000):
    print(i)
    league = League()
    clubs = [Club() for i in range(20)]
    features = clubs[0].features.keys()
    league.populateWithClubs(clubs)
    league.setGlobalFeatures()
    league.schedule()
    for gameweek in league.schedule:
        for clubs in gameweek.values():
            match = Match(league, clubs[0], clubs[1])
            match.play()
    for rank, (club, _) in enumerate(sorted(league.leagueTable.items(), key = lambda x: (x[1]['Pts'], x[1]['GD']), reverse = True), 1):
        data.append(
            {
                'features': {feature: club.features[feature] for feature in features},
                'labels': {'rank': rank}
            }
        )

try:
    Utils.pickleObject(data)
except:
    catcherInTheRye = 1

print(datetime.now())

### Would be cool to run tests such as increasing injury rate to see if this strengthens the negative correlation between depth and rank (as expected)