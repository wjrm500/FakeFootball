import numpy as np

class Tournament:
    def __init__(self, system):
        self.system = system
        self.matchReports = []

    def populateWithClubs(self, clubs):
        self.clubs = []
        for club in clubs:
            self.clubs.append(club)
        self.numClubs = len(self.clubs)
    
    def playOutstandingFixtures(self, date):
        for fixture in self.fixtures:
            if fixture.date == date:
                fixture.play()

    def handleMatchReport(self, matchReport):
        self.matchReports.append(matchReport)
        for club, clubReport in matchReport['clubs'].items():
            for player, playerReport in clubReport['players'].items():
                player.matchReports.append(playerReport)

    def getPerformanceIndices(
        self,
        indices = ['games', 'goals', 'assists', 'performanceIndex'],
        sortBy = None,
        sortDir = None,
        clubs = None
        ):
        performanceIndices = {}
        clubs = clubs if clubs is not None else self.clubs
        clubs = clubs if type(clubs) == list else [clubs]
        for club in clubs:
            for player in club.squad:
                performanceIndices[player] = {}
                if 'rating' in indices:
                    performanceIndices[player]['rating'] = player.rating
                if 'games' in indices:
                    performanceIndices[player]['games'] = np.sum([1 for matchReport in player.matchReports if matchReport['tournament'] == self])
                if 'goals' in indices:
                    performanceIndices[player]['goals'] = np.sum([matchReport['goals'] for matchReport in player.matchReports if matchReport['tournament'] == self])
                if 'assists' in indices:
                    performanceIndices[player]['assists'] = np.sum([matchReport['assists'] for matchReport in player.matchReports if matchReport['tournament'] == self])
                if 'performanceIndex' in indices:
                    performanceIndices[player]['performanceIndex'] = np.mean([matchReport['performanceIndex'] for matchReport in player.matchReports if matchReport['tournament'] == self])
                    if np.isnan(performanceIndices[player]['performanceIndex']):
                        performanceIndices[player]['performanceIndex'] = 0
                if 'positions' in indices:
                    performanceIndices[player]['positions'] = {position: [matchReport['position'] for matchReport in player.matchReports if matchReport['tournament'] == self].count(position) for position in set([matchReport['position'] for matchReport in player.matchReports if matchReport['tournament'] == self])}
        if sortBy is not None:
            return sorted(performanceIndices.items(), key = lambda x: x[1][sortBy], reverse = False if sortDir == 'asc' else True)
        return [performanceIndices]
    
    def displayPerformanceIndices(
        self,
        indices = ['rating', 'games', 'goals', 'assists', 'performanceIndex'],
        positions = ['CF', 'WF', 'COM', 'WM', 'CM', 'CDM', 'WB', 'FB', 'CB'],
        clubs = None,
        sortBy = None,
        sortDir = None,
        limit = None
        ):
        allPerformanceIndices = self.getPerformanceIndices(
            indices,
            sortBy,
            sortDir,
            clubs
        )
        limit = limit if limit is not None else len(allPerformanceIndices)
        recordsPrinted = 0
        for instance in allPerformanceIndices:
            player = instance[0]
            performanceIndices = instance[1]
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