import sys
sys.path.append('.')
from Tournaments.League import League
import random

class Group(League):   
    def __init__(self, tournament):
        self.tournament = tournament
        self.universe = self.tournament.universe
        super().__init__(None, None)
    
    def handleMatchReport(self, matchReport):
        super().handleMatchReport(matchReport)
        self.tournament.handleMatchReport(matchReport)
    
    def getNumPlaceholders(self):
        return sum([1 for club in self.clubs if type(club) == dict])

    def replacePlaceholderWithClub(self, newClub):
        availableKeys = []
        for existingClub in self.clubs:
            if type(existingClub) == dict:
                availableKeys.append(list(existingClub.keys())[0])
        randomlySelectedKey = random.choice(availableKeys)
        for existingClub in self.clubs:
            if type(existingClub) == dict:
                if list(existingClub.keys())[0] == randomlySelectedKey:
                    replacementIndex = self.clubs.index(existingClub)
                    self.clubs[replacementIndex] = newClub
                    break
        for fixture in self.tournament.fixtures:
            for existingClub in fixture.clubs:
                if type(existingClub) == dict:
                    if list(existingClub.keys())[0] == randomlySelectedKey:
                        replacementIndex = fixture.clubs.index(existingClub)
                        if replacementIndex == 0:
                            fixture.clubX = newClub
                        elif replacementIndex == 1:
                            fixture.clubY = newClub
                        fixture.clubs[replacementIndex] = newClub
                        break
        self.leagueTables[0][newClub] = {}
        for stat in ['GP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']:
            self.leagueTables[0][newClub][stat] = 0