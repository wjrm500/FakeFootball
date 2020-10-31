import Utilities.Utils as Utils
from config import systemConfig
from PersonController import PersonController
import random
import numpy as np
from Database import Database

class Club:
    def __init__(self, name, manager = None, squad = None):
        self.name = name
        self.transferBudget = 0
    
    def setLeague(self, league):
        self.league = league
        self.system = league.system
        
    def populateSquad(self, squad = None):
        self.squad = []
        if squad is None:
            while len(self.squad) < systemConfig['numPlayersPerClub']:
                personController = PersonController()
                player = random.choice(personController.freeAgentPlayers)
                personController.freeAgentPlayers.remove(player)
                self.addFreeAgentPlayer(player)
    
    def addFreeAgentPlayer(self, player):
        self.squad.append(player)
        player.club = self
    
    def addFreeAgentManager(self, manager = None):
        if manager is None:
            personController = PersonController()
            manager = random.choice(personController.freeAgentManagers)
            personController.freeAgentManagers.remove(manager)
        self.manager = manager
        manager.club = self
    
    def getRating(self):
        return np.mean([player.rating for player in self.squad])
    
    def getPlayersSortedByRating(self):
        squadCopy = self.squad.copy()
        squadCopy.sort(key = lambda x: x.rating, reverse = True)
        return squadCopy
    
    def displayPerformanceIndices(self):
        comp1 = self.league
        comp2 = self.system.systemKnockout
        comp3 = self.system.universe.superiorUniversalTournament
        comp4 = self.system.universe.inferiorUniversalTournament
        competitions = [comp1, comp2, comp3, comp4]
        shortenedCompNames = '{:^23} {:^23} {:^23} {:^23} {:^23}'.format('League', 'System Knockout', 'Superior Universal', 'Inferior Universal', 'Total')
        print('{}{}'.format(' ' * 41, shortenedCompNames))
        print('-' * 157)
        subHeading = 'GP /  G /  A /   PI'
        subHeadings = '{:^23} {:^23} {:^23} {:^23} {:^23}'.format(subHeading, subHeading, subHeading, subHeading, subHeading)
        print('{}{}'.format(' ' * 40, subHeadings))
        print('-' * 157)
        for player in self.getPlayersSortedByRating():
            player.displayOneLinePerformanceIndices(competitions)