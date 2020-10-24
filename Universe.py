from System import System
from config import systemConfig
import Utilities.Utils as Utils
import copy
from PersonController import PersonController
import numpy as np

class _Universe:
    def __init__(self, timeLord, config):
        self.timeLord = timeLord
        self.config = copy.deepcopy(systemConfig)
        if config is not None and config != systemConfig:
            Utils.updateConfig(self.config, config)
        self.personController = PersonController(self)
        self.systems = []
    
    def populate(self):
        for _ in range(self.config['numSystems']):
            self.addSystem()
        self.personController.populateActiveManagerPool(np.product(list(self.config.values())[:-1]))
        self.personController.populateActivePlayerPool(np.product(list(self.config.values())))
        for system in self.systems:
            system.addLeagues()
            system.addSystemKnockout()
            system.addClubs()
            for club in system.clubs:
                club.addFreeAgentManager()
                club.populateSquad()
            system.clubs.sort(key = lambda x: x.getAverageRating(), reverse = True)
            system.populateLeaguesWithClubs()
            system.systemKnockout.populateWithClubs()
            system.systemKnockout.setStages()
        
    def addSystem(self, name = None):
        self.systems.append(System(self, name))
    
    def removeSystem(self, name):
        del self.systems[name]
    
    def playFixtures(self, date):
        for system in self.systems:
            for tournament in system.tournaments:
                tournament.playOutstandingFixtures(date)


_instance = None

def Universe(timeLord, config = None):
    global _instance
    if _instance is None:
        _instance = _Universe(timeLord, config)
    return _instance