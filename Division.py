from Club import Club
from Match import Match
import Utilities.Utils as Utils
import numpy as np

class Division:
    def __init__(self, system, systemConfig):
        self.system = system
        self.clubs = [Club(self) for _ in range(systemConfig['numTeamsPerDivision'])]
        self.players = [player for club in self.clubs for player in club.squad]
        self.schedule = {}
        self.league = {}
        for club in self.clubs:
            self.league[club] = {}
            for stat in ['GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']:
                self.league[club][stat] = 0
        self.goalscorers = []
        self.assisters = []
        self.playerStats = {}
        self.reports = []
    
    def scheduleFixture(self, date, clubX, clubY):
        if not self.schedule.get(date): ### If date exists
            self.schedule[date] = []
        self.schedule[date].append([clubX, clubY])
    
    def playFixture(self, date, fixture):
        clubX, clubY = fixture[0], fixture[1]
        match = Match(self, date, clubX, clubY)
        match.play()
        match.fileMatchReport()
    
    def handleMatchReport(self, matchReport):
        self.reports.append(matchReport)
        for club, clubReport in matchReport['clubs'].items():
            self.league[club]['GP'] += 1
            self.league[club]['GF'] += clubReport['match']['goalsFor']
            self.league[club]['GA'] += clubReport['match']['goalsAgainst']
            self.league[club]['GD'] += clubReport['match']['goalsFor'] - clubReport['match']['goalsAgainst']
            if clubReport['match']['outcome'] == 'win':
                self.league[club]['W'] += 1
                self.league[club]['Pts'] += 3
            elif clubReport['match']['outcome'] == 'draw':
                self.league[club]['D'] += 1
                self.league[club]['Pts'] += 1
            elif clubReport['match']['outcome'] == 'loss':
                self.league[club]['L'] += 1
            self.goalscorers.extend(clubReport['match']['goalscorers'])
            self.assisters.extend(clubReport['match']['assisters'])
            for player, playerReport in clubReport['players'].items():
                if not self.playerStats.get(player):
                    self.playerStats[player] = []
                self.playerStats[player].append(playerReport)
                player.matchReports.append(playerReport)
    
    def displayLeagueTable(self):
        sortedClubs = sorted(self.league.items(), key = lambda x: x[1]['Pts'], reverse = True)
        for i, (club, data) in enumerate(sortedClubs):
            x = '{:2}. {} --- '.format(i + 1, club.name)
            for key, value in data.items():
                x += '{}: {:3}     '.format(key, value)
            team = club.manager.selectTeam()
            x += 'Offence: {} --- Defence: {}'.format(int(round(team.offence)), int(round(team.defence)))
            print(x)
        print('\n')
    
    def getPlayerStats(self, stat):
        if stat == 'goals':
            l = self.goalscorers
        elif stat == 'assists':
            l = self.assisters
        x = [{'player': player, stat: l.count(player)} for player in set(l)]
        x = sorted(x, key = lambda k: k[stat], reverse = True)
        return x
    
    def displayPlayerStats(self, stat, numRecords):
        x = self.getPlayerStats(stat)
        for item in x[0:numRecords]:
            playerName = ' '.join(item['player'].properName)
            club = item['player'].club.name
            numItems = item[stat]
            ratPos = '{} rated {}'.format(str(int(round(item['player'].rating))), item['player'].bestPosition)
            print('Player: {:30} - {:12} - Club: {} - {:2} {}'.format(playerName, ratPos, club, numItems, stat))
    
    def getBestPlayers(self, position):
        sortedPlayers = sorted(self.players, key = lambda x: x.rating, reverse = True)
        if position is not None:
            sortedPlayers = [player for player in sortedPlayers if player.bestPosition == position]
        return sortedPlayers
    
    def displayBestPlayers(self, position = None, numRecords = 5):
        x = self.getBestPlayers(position)
        for player in x[0:numRecords]:
            playerName = player.properName
            club = player.club.name
            ratPos = '{} rated {}'.format(str(int(round(player.rating))), player.bestPosition)
            numGoals = self.goalscorers.count(player)
            numAssists = self.assisters.count(player)
            print('Player: {:30} - {:12} - Club: {} - {:2} goals and {:2} assists'.format(playerName, ratPos, club, numGoals, numAssists))
        
    def getSeasonPerformanceIndices(
        self,
        indices = ['games', 'goals', 'assists', 'performanceIndex'],
        sortBy = None,
        sortDir = None,
        clubs = None
        ):
        seasonPerformanceIndices = {}
        clubs = clubs if clubs is not None else self.clubs
        clubs = clubs if type(clubs) == list else [clubs]
        for club in clubs:
            for player in club.squad:
                seasonPerformanceIndices[player] = {}
                if 'rating' in indices:
                    seasonPerformanceIndices[player]['rating'] = player.rating
                if 'games' in indices:
                    seasonPerformanceIndices[player]['games'] = np.sum([1 for matchReport in player.matchReports])
                if 'goals' in indices:
                    seasonPerformanceIndices[player]['goals'] = np.sum([matchReport['goals'] for matchReport in player.matchReports])
                if 'assists' in indices:
                    seasonPerformanceIndices[player]['assists'] = np.sum([matchReport['assists'] for matchReport in player.matchReports])
                if 'performanceIndex' in indices:
                    seasonPerformanceIndices[player]['performanceIndex'] = np.mean([matchReport['performanceIndex'] for matchReport in player.matchReports])
                    if np.isnan(seasonPerformanceIndices[player]['performanceIndex']):
                        seasonPerformanceIndices[player]['performanceIndex'] = 0
                if 'positions' in indices:
                    seasonPerformanceIndices[player]['positions'] = {position: [matchReport['position'] for matchReport in player.matchReports].count(position) for position in set([matchReport['position'] for matchReport in player.matchReports])}
        if sortBy is not None:
            return sorted(seasonPerformanceIndices.items(), key = lambda x: x[1][sortBy], reverse = False if sortDir == 'asc' else True)
        return seasonPerformanceIndices
    
    def displaySeasonPerformanceIndices(
        self,
        indices = ['rating', 'games', 'goals', 'assists', 'performanceIndex'],
        positions = ['CF', 'WF', 'COM', 'WM', 'CM', 'CDM', 'WB', 'FB', 'CB'],
        clubs = None,
        sortBy = None,
        sortDir = None,
        limit = None
        ):
        seasonPerformanceIndices = self.getSeasonPerformanceIndices(
            indices,
            sortBy,
            sortDir,
            clubs
        )
        limit = limit if limit is not None else len(seasonPerformanceIndices)
        recordsPrinted = 0
        for player, performanceIndices in seasonPerformanceIndices:
            if recordsPrinted == limit:
                break
            if player.bestPosition in positions:
                printArray = []
                printArray.append('{:4} - {:30} - {} rated {:3}'.format(player.id, player.properName, int(player.rating), player.bestPosition))
                for performanceIndex, value in performanceIndices.items():
                    if performanceIndex == 'rating':
                        continue
                    elif performanceIndex == 'performanceIndex':
                        printArray.append('{}: {:.2f}'.format(performanceIndex, value))
                    elif performanceIndex == 'positions':
                        printArray.append('{}: {}'.format(performanceIndex, value))
                    else:
                        printArray.append('{}: {:2}'.format(performanceIndex, int(value)))
                print(' --- '.join(printArray))
                recordsPrinted += 1