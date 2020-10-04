from Division import Division
from Player import Player
from schedule import schedule
from MatchEngine import MatchEngine
from Manager import Manager
from collections import Counter
import numpy as np

division = Division()
for club in division.clubs.values():
    for i in range(40):
        player = Player()
        if player.retired is False:
            club.signPlayer(player)
    club.hireManager(Manager())

leagueTable = {}
for club in division.clubs.values():
    leagueTable[club] = {}
    for column in ['GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']:
        leagueTable[club][column] = 0

leagueGoalscorers, leagueAssisters = [], []
for gameweek in range(1, 39):
    for fixture in schedule[gameweek]:
        homeClub = division.clubs[fixture['homeSlot']]
        awayClub = division.clubs[fixture['awaySlot']]
        matchEngine = MatchEngine(homeClub, awayClub)
        matchEngine.playMatch()
        matchReport = matchEngine.fileMatchReport()
        for club in [homeClub, awayClub]:
            report = matchReport[club]
            leagueTable[club]['GP'] += 1
            leagueTable[club]['GF'] += report['match']['goalsFor']
            leagueTable[club]['GA'] += report['match']['goalsAgainst']
            leagueTable[club]['GD'] += report['match']['goalsFor'] - report['match']['goalsAgainst']
            if report['match']['outcome'] == 'win':
                leagueTable[club]['W'] += 1
                leagueTable[club]['Pts'] += 3
            elif report['match']['outcome'] == 'draw':
                leagueTable[club]['D'] += 1
                leagueTable[club]['Pts'] += 1
            elif report['match']['outcome'] == 'loss':
                leagueTable[club]['L'] += 1
            leagueGoalscorers.append(report['match']['goalscorers'])
            leagueAssisters.append(report['match']['assisters'])

leagueGoalscorers = [goalscorer for gameGoalscorers in leagueGoalscorers for goalscorer in gameGoalscorers]
leagueAssisters = [assister for gameAssisters in leagueAssisters for assister in gameAssisters]

sortedClubs = sorted(leagueTable.items(), key = lambda x: x[1]['Pts'], reverse = True)
for i, (club, data) in enumerate(sortedClubs):
    x = '{:2}. {} --- '.format(i + 1, club.name)
    for key, value in data.items():
        x += '{}: {:3}     '.format(key, value)
    team = club.manager.selectTeam()
    x += 'Offence: {} --- Defence: {}'.format(int(round(team.offence)), int(round(team.defence)))
    print(x)
print('\n')

for y, z in zip(
    [
        leagueGoalscorers,
        leagueAssisters,
        leagueGoalscorers + leagueAssisters
    ],
    [
        'goals',
        'assists',
        'goals and assists'
    ]
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
            numGoals = leagueGoalscorers.count(item['player'])
            numAssists = leagueAssisters.count(item['player'])
            print('Player: {} - {} - Club: {} - {:2} goals and {:2} assists'.format(playerName, ratPos, club, numGoals, numAssists))
    print('\n')

players = [player for club in division.clubs.values() for player in club.squad]
sortedPlayers = sorted(players, key = lambda x: x.rating, reverse = True)
print('Best players by rating:')
for player in sortedPlayers[0:5]:
    playerName = player.name
    club = player.club.name
    ratPos = '{} rated {}'.format(str(int(round(player.rating))), player.bestPosition)
    numGoals = leagueGoalscorers.count(player)
    numAssists = leagueAssisters.count(player)
    print('Player: {} - {} - Club: {} - {:2} goals and {:2} assists'.format(playerName, ratPos, club, numGoals, numAssists))

print('hello')