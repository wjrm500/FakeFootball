import numpy as np

class Tournament:
    def __init__(self, system):
        self.system = system
        yearAsString = str(self.universe.timeLord.currentDate.year) if self.system is None else str(self.system.universe.timeLord.currentDate.year)
        self.name = type(self).__name__ + yearAsString
        self.matchReports = []
        self.clubs = []
        self.numClubs = 0

    def populateWithClubs(self, clubs):
        for club in clubs:
            self.clubs.append(club)
            self.numClubs += 1
    
    def playOutstandingFixtures(self, date):
        for fixture in self.fixtures:
            if fixture.date == date:
                fixture.play()

    def handleMatchReport(self, matchReport):
        self.matchReports.append(matchReport)
        for club, clubReport in matchReport['clubs'].items():
            for player, playerReport in clubReport['players'].items():
                player.handlePlayerReport(playerReport)

    def getPerformanceIndices(
        self,
        indices = ['games', 'goals', 'assists', 'performanceIndex'],
        upToGameweek = None,
        sortBy = None,
        sortDir = None,
        clubs = None
        ):
        performanceIndices = {}
        clubs = clubs if clubs is not None else self.clubs
        clubs = clubs if type(clubs) == list else [clubs]
        upToGameweek = self.numClubs * 2 - 1 if upToGameweek is None else upToGameweek
        for club in clubs:
            club = self.universe.getClubByName(club) if type(club) == str else club
            for player in club.squad:
                gamesPlayed = np.sum([1 for playerReport in player.playerReports if playerReport['tournament'] == self and playerReport['gameweek'] <= upToGameweek])
                performanceIndices[player] = {}
                if 'rating' in indices:
                    performanceIndices[player]['rating'] = player.rating
                if 'games' in indices:
                    performanceIndices[player]['games'] = gamesPlayed
                if 'goals' in indices:
                    performanceIndices[player]['goals'] = np.sum([playerReport['goals'] for playerReport in player.playerReports if playerReport['tournament'] == self and playerReport['gameweek'] <= upToGameweek])
                if 'assists' in indices:
                    performanceIndices[player]['assists'] = np.sum([playerReport['assists'] for playerReport in player.playerReports if playerReport['tournament'] == self and playerReport['gameweek'] <= upToGameweek])
                if 'performanceIndex' in indices:
                    performanceIndices[player]['performanceIndex'] = np.mean([playerReport['performanceIndex'] for playerReport in player.playerReports if playerReport['tournament'] == self and playerReport['gameweek'] <= upToGameweek])
                    ### If player has appeared in less than half of the games they are ineligible for Performance Index ranking
                    if gamesPlayed < upToGameweek / 2 or np.isnan(performanceIndices[player]['performanceIndex']):
                        performanceIndices[player]['performanceIndex'] = 0
                if 'positions' in indices:
                    performanceIndices[player]['positions'] = {position: [playerReport['position'] for playerReport in player.playerReports if playerReport['tournament'] == self and playerReport['gameweek'] <= upToGameweek].count(position) for position in set([playerReport['position'] for playerReport in player.playerReports if playerReport['tournament'] == self and playerReport['gameweek'] <= upToGameweek])}
        if sortBy is not None:
            sortedList = sorted(performanceIndices.items(), key = lambda x: x[1][sortBy], reverse = False if sortDir == 'asc' else True)
            performanceIndices = {player: performanceIndices for player, performanceIndices in sortedList}
        return performanceIndices
    
    def displayPerformanceIndices(
        self,
        indices = ['rating', 'games', 'goals', 'assists', 'performanceIndex'],
        positions = ['CF', 'WF', 'COM', 'WM', 'CM', 'CDM', 'WB', 'FB', 'CB'],
        clubs = None,
        upToGameweek = None,
        sortBy = None,
        sortDir = None,
        limit = None
        ):
        allPerformanceIndices = self.getPerformanceIndices(
            indices,
            upToGameweek,
            sortBy,
            sortDir,
            clubs
        )
        limit = limit if limit is not None else len(allPerformanceIndices)
        recordsPrinted = 0
        for player, performanceIndices in allPerformanceIndices.items():
            if recordsPrinted == limit:
                break
            if player.bestPosition in positions:
                printArray = []
                printArray.append('{:4} - {:30} - {:21} - {} rated {:3}'.format(
                    player.id,
                    player.properName,
                    player.club.name,
                    int(player.rating),
                    player.bestPosition
                    )
                )
                for performanceIndex, value in performanceIndices.items():
                    shortener = {'games': 'GP', 'goals': 'G', 'assists': 'A', 'performanceIndex': 'PI'}
                    if performanceIndex == 'rating':
                        continue
                    elif performanceIndex == 'performanceIndex':
                        printArray.append('{}: {:.2f}'.format(shortener[performanceIndex], value))
                    elif performanceIndex == 'positions':
                        printArray.append('{}: {}'.format(shortener[performanceIndex], value))
                    else:
                        printArray.append('{}: {:2}'.format(shortener[performanceIndex], int(value)))
                print(' - '.join(printArray))
                recordsPrinted += 1