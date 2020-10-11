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
        self.playerStats = {}
    
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
        for club, clubReport in matchReport.items():
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
            playerName = ' '.join(item['player'].name)
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
            playerName = player.name
            club = player.club.name
            ratPos = '{} rated {}'.format(str(int(round(player.rating))), player.bestPosition)
            numGoals = self.goalscorers.count(player)
            numAssists = self.assisters.count(player)
            print('Player: {} - {} - Club: {} - {:2} goals and {:2} assists'.format(playerName, ratPos, club, numGoals, numAssists))