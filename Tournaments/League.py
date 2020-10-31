import sys
sys.path.append('.')
from Club import Club
from Match import Match
import Utilities.Utils as Utils
import numpy as np
from Tournaments.Tournament import Tournament
import random

class League(Tournament):   
    def __init__(self, system, tier):
        super().__init__(system)
        self.tier = tier
    
    def populateWithClubs(self, clubs):
        super().populateWithClubs(clubs)
        if type(self).__name__ != "Group":
            for club in clubs:
                club.setLeague(self)
        self.leagueTable = {}
        for club in self.clubs:
            if type(club).__name__ == 'Club':
                self.leagueTable[club] = {}
                for stat in ['GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']:
                    self.leagueTable[club][stat] = 0
    
    def handleMatchReport(self, matchReport):
        super().handleMatchReport(matchReport)
        for club, clubReport in matchReport['clubs'].items():    
            self.leagueTable[club]['GP'] += 1
            self.leagueTable[club]['GF'] += clubReport['match']['goalsFor']
            self.leagueTable[club]['GA'] += clubReport['match']['goalsAgainst']
            self.leagueTable[club]['GD'] += clubReport['match']['goalsFor'] - clubReport['match']['goalsAgainst']
            if clubReport['match']['outcome'] == 'win':
                self.leagueTable[club]['W'] += 1
                self.leagueTable[club]['Pts'] += 3
            elif clubReport['match']['outcome'] == 'draw':
                self.leagueTable[club]['D'] += 1
                self.leagueTable[club]['Pts'] += 1
            elif clubReport['match']['outcome'] == 'loss':
                self.leagueTable[club]['L'] += 1
    
    def displayLeagueTable(self):
        sortedClubs = sorted(self.leagueTable.items(), key = lambda x: x[1]['Pts'], reverse = True)
        for i, (club, data) in enumerate(sortedClubs):
            x = '{:2}. {:21} --- '.format(i + 1, club.name)
            for key, value in data.items():
                x += '{}: {:3}     '.format(key, value)
            team = club.manager.selectTeam()
            x += 'Offence: {} --- Defence: {}'.format(int(round(team.offence)), int(round(team.defence)))
            print(x)
        print('\n')
    
    def checkComplete(self):
        return all([fixture.played for fixture in self.fixtures])
    
    def getClubByRank(self, rank):
        sortedClubs = sorted(self.leagueTable.items(), key = lambda x: x[1]['Pts'], reverse = True)
        return sortedClubs[rank][0] ### Does this return a club?