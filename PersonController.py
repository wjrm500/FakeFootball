from Persons.Player import Player
from Persons.Manager import Manager
import random

class _PersonController:
    def __init__(self):
        self.players = []
        self.managers = []
    
    def createPlayer(self, player = None):
        player = Player() if player is None else player
        self.players.append(player)
        return player
    
    def createManager(self, manager = None):
        manager = Manager() if manager is None else manager
        self.managers.append(manager)
        return manager
    
    def getRandomFreeAgent(self):
        return random.choice(self.players['freeAgents'])

_instance = None

def PersonController():
    global _instance
    if _instance is None:
        _instance = _PersonController()
    return _instance