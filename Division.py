from Club import Club
from Match import Match

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
    
    def scheduleFixture(self, date, clubX, clubY):
        if not self.schedule.get(date): ### If date exists
            self.schedule[date] = []
        self.schedule[date].append([clubX, clubY])
    
    def playFixture(self, fixture):
        clubX, clubY = fixture[0], fixture[1]
        match = Match(self, clubX, clubY)
        match.play()
        match.fileMatchReport()
    
    def handleMatchReport(self, matchReport):
        for club, report in matchReport.items():
            self.league[club]['GP'] += 1
            self.league[club]['GF'] += report['match']['goalsFor']
            self.league[club]['GA'] += report['match']['goalsAgainst']
            self.league[club]['GD'] += report['match']['goalsFor'] - report['match']['goalsAgainst']
            if report['match']['outcome'] == 'win':
                self.league[club]['W'] += 1
                self.league[club]['Pts'] += 3
            elif report['match']['outcome'] == 'draw':
                self.league[club]['D'] += 1
                self.league[club]['Pts'] += 1
            elif report['match']['outcome'] == 'loss':
                self.league[club]['L'] += 1
            self.goalscorers.extend(report['match']['goalscorers'])
            self.assisters.extend(report['match']['assisters'])
    
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
    
    def displayBestPlayers(self, numPlayers = 5):
        sortedPlayers = sorted(self.players, key = lambda x: x.rating, reverse = True)
        print('Best players by rating:')
        for player in sortedPlayers[0:numPlayers]:
            playerName = player.name
            club = player.club.name
            ratPos = '{} rated {}'.format(str(int(round(player.rating))), player.bestPosition)
            numGoals = self.goalscorers.count(player)
            numAssists = self.assisters.count(player)
            print('Player: {} - {} - Club: {} - {:2} goals and {:2} assists'.format(playerName, ratPos, club, numGoals, numAssists))