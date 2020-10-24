import Utilities.Utils as Utils
from config import systemConfig
from PersonController import PersonController
import random
import numpy as np

class Club:
    def __init__(self, league = None, name = None, manager = None, squad = None):
        if league is not None:
            self.system = league.system
            self.league = league
        self.name = Utils.generateName(8) if name is None else name
        self.transferBudget = 0
        
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
    
    def getAverageRating(self):
        return np.mean([player.rating for player in self.squad])