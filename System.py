from Division import Division
import Utilities.Utils as Utils

class System:
    def __init__(self, systemConfig, name = None):
        self.name = Utils.generateName(4) if name is None else name
        self.divisions = [Division(self, systemConfig) for _ in range(systemConfig['numDivisionsPerSystem'])]
    
    def displayTopScorersAssisters(self):
        for y, z in zip(
            [self.goalscorers, self.assisters, self.goalscorers + self.assisters],
            ['goals', 'assists', 'goals and assists']
            ):
            print('Top ranked players for {}:'.format(z))
            y = [{'player': player, z: y.count(player)} for player in set(y)]
            y = sorted(y, key = lambda x: x[z], reverse = True)
            for item in y[0:5]:
                playerName = item['player'].name
                club = item['player'].club.name
                numItems = item[z]
                ratPos = '{} rated {}'.format(str(int(round(item['player'].rating))), item['player'].bestPosition)
                if z in ['goals', 'assists']:
                    print('Player: {} - {} - Club: {} - {:2} {}'.format(playerName, ratPos, club, numItems, z))
                elif z == 'goals and assists':
                    numGoals = self.goalscorers.count(item['player'])
                    numAssists = self.assisters.count(item['player'])
                    print('Player: {} - {} - Club: {} - {:2} goals and {:2} assists'.format(playerName, ratPos, club, numGoals, numAssists))
            print('\n')