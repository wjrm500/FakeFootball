import sys
sys.path.append('.')
from Club import Club
from Match import Match
import Utilities.Utils as Utils
import numpy as np
from Tournaments.Tournament import Tournament
import random
import copy

class League(Tournament):   
    def __init__(self, system, tier):
        super().__init__(system)
        self.tier = tier
    
    def populateWithClubs(self, clubs):
        super().populateWithClubs(clubs)
        if type(self).__name__ != "Group":
            for club in clubs:
                club.setLeague(self)
        self.leagueTables = {0: {}}
        for club in self.clubs:
            if type(club).__name__ == 'Club':
                self.leagueTables[0][club] = {}
                for stat in ['GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']:
                    self.leagueTables[0][club][stat] = 0
    
    def getFeature(self, featureName):
        if not hasattr(self, 'features'):
            strengths, depths = [], []
            for club in self.clubs:
                strengths.append(club.features['strength'])
                depths.append(club.features['depth'])
            self.features = {
                'meanStrength': np.mean(strengths),
                'meanDepth': np.mean(depths)
            }
        return self.features[featureName]
    
    def handleMatchReport(self, matchReport):
        super().handleMatchReport(matchReport)
        maxGamesPlayed = max(self.leagueTables.keys())
        gameweekProgression = len(set([value['GP'] for value in self.leagueTables[maxGamesPlayed].values()])) == 1
        if gameweekProgression:
            currentGameweek = maxGamesPlayed + 1
            self.leagueTables[currentGameweek] = {club: copy.deepcopy(self.leagueTables[maxGamesPlayed][club]) for club in self.clubs}
        else:
            currentGameweek = maxGamesPlayed
        for club, clubReport in matchReport['clubs'].items():
            self.leagueTables[currentGameweek][club]['GP'] += 1
            self.leagueTables[currentGameweek][club]['GF'] += clubReport['match']['goalsFor']
            self.leagueTables[currentGameweek][club]['GA'] += clubReport['match']['goalsAgainst']
            self.leagueTables[currentGameweek][club]['GD'] += clubReport['match']['goalsFor'] - clubReport['match']['goalsAgainst']
            if clubReport['match']['outcome'] == 'win':
                self.leagueTables[currentGameweek][club]['W'] += 1
                self.leagueTables[currentGameweek][club]['Pts'] += 3
            elif clubReport['match']['outcome'] == 'draw':
                self.leagueTables[currentGameweek][club]['D'] += 1
                self.leagueTables[currentGameweek][club]['Pts'] += 1
            elif clubReport['match']['outcome'] == 'loss':
                self.leagueTables[currentGameweek][club]['L'] += 1
    
    def getLeagueTable(self, gameweek = 38, positions = None, simplified = False, display = False):
        leagueTable = self.leagueTables[gameweek]
        allSortedClubs = sorted(leagueTable.items(), key = lambda x: (x[1]['Pts'], x[1]['GD'], x[1]['GF']), reverse = True)
        if positions is not None:
            if isinstance(positions, int):
                sortedClubs = allSortedClubs[positions - 1]
            elif isinstance(positions, tuple):
                sortedClubs = allSortedClubs[positions[0] - 1:positions[1]]
            if not isinstance(sortedClubs, list):
                sortedClubs = [sortedClubs]
        else:
            sortedClubs = copy.copy(allSortedClubs)
        if not display:
            printArray = []
        for rank, (club, data) in enumerate(sortedClubs, 1):
            if positions is not None:
                rank = allSortedClubs.index(list(filter(lambda tup: tup[0] == club, allSortedClubs))[0]) + 1
            if simplified:
                x = '{:<2}. {:5} '.format(str(rank), club.getShortName())
            else:
                x = '{:<2}. {:21} '.format(str(rank), club.name)
            if simplified:
                x += '{:3}'.format(data['Pts'])
            else:
                for key, value in data.items():
                    x += '{}: {:3}     '.format(key, value)
            if not simplified:
                x += 'Rating: {}'.format(club.getRating())
            if not display:
                printArray.append(x.strip())
            else:
                print(x.strip())
        if not display:
            if len(printArray) == 1:
                return printArray[0]
            return printArray
    
    def checkComplete(self):
        return all([fixture.played for fixture in self.fixtures])
    
    def getClubByRank(self, rank):
        finalGameweek = max(self.leagueTables.keys())
        sortedClubs = sorted(self.leagueTables[finalGameweek].items(), key = lambda x: x[1]['Pts'], reverse = True)
        return sortedClubs[rank][0] ### Does this return a club?