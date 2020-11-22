import copy
import numpy as np

class League:
    def populateWithClubs(self, clubs):
        self.clubs = []
        self.leagueTable = {}
        for club in clubs:
            self.clubs.append(club)
            self.leagueTable[club] = {}
            for stat in ['GP', 'GD', 'Pts']:
                self.leagueTable[club][stat] = 0
    
    def setGlobalFeatures(self):
        strengths, depths = [], []
        for club in self.clubs:
            strengths.append(club.features['strength'])
            depths.append(club.features['depth'])
        globalFeatures = {
            'meanStrength': np.mean(strengths),
            'meanDepth': np.mean(depths)
        }
        for club in self.clubs:
            club.features['strength'] /= globalFeatures['meanStrength']
            club.features['depth'] /= globalFeatures['meanDepth']

    def handleMatchReport(self, matchReport):
        for club, clubReport in matchReport['clubs'].items():
            self.leagueTable[club]['GP'] += 1
            self.leagueTable[club]['GD'] += clubReport['match']['goalsFor'] - clubReport['match']['goalsAgainst']
            if clubReport['match']['outcome'] == 'win':
                self.leagueTable[club]['Pts'] += 3
            elif clubReport['match']['outcome'] == 'draw':
                self.leagueTable[club]['Pts'] += 1
            for player, playerReport in clubReport['players'].items():
                player.handlePlayerReport(playerReport)
    
    def schedule(self):
        numClubs = len(self.clubs)
        schedule = []
        fixturesPerWeek = int(numClubs / 2)
        maxIndex = fixturesPerWeek - 1
        for i in range(numClubs - 1):
            newGameweek = {}
            if i == 0:
                clubsForPopping = copy.copy(self.clubs)
                for j in range(fixturesPerWeek):
                    newGameweek[j] = [clubsForPopping.pop(0), clubsForPopping.pop()]
            else:
                lastGameweek = schedule[i - 1]
                for j in range(fixturesPerWeek):
                    if j == 0:
                        clubOne = self.clubs[0]
                    elif j == 1:
                        clubOne = lastGameweek[0][1]
                    else:
                        clubOne = lastGameweek[j - 1][0]

                    if j != maxIndex:
                        clubTwo = lastGameweek[j + 1][1]
                    else:
                        clubTwo = lastGameweek[maxIndex][0]
                    
                    newGameweek[j] = [clubOne, clubTwo]
            schedule.append(newGameweek)
        for i, gameweek in enumerate(schedule):
            if i % 2 != 0: ### If index is odd - to only flip teams on alternate gameweeks
                for key, value in gameweek.items():
                    gameweek[key] = [value[1], value[0]] ### Flip home and away teams
        flippedSchedule = [copy.copy(gameweek) for gameweek in schedule] ### copy.copy(schedule) does not work because the list objects containing clubs in schedule are mutated // copy.deepcopy(schedule) does not work because club objects are duplicated so effectively a separate set of clubs is referenced in second half of schedule
        for i, gameweek in enumerate(flippedSchedule):
            for key, value in gameweek.items():
                gameweek[key] = [value[1], value[0]] ### Flip home and away teams
        self.schedule = schedule + flippedSchedule
    
    def getClubByRank(self, rank):
        sortedClubs = sorted(self.leagueTable.items(), key = lambda x: x[1]['Pts'], reverse = True)
        return sortedClubs[rank][0]