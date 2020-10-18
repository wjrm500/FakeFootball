from Persons.Player import Player
from Persons.Manager import Manager
import random
import numpy as np
from datetime import date, timedelta
import copy

class _PersonController:
    def __init__(self, universe):
        self.universe = universe
        self.players, self.playersCreated = [], 0
        self.activePlayers, self.retiredPlayers, self.freeAgentPlayers = [], [], []
        self.managers, self.managersCreated = [], 0
        self.activeManagers, self.retiredManagers, self.freeAgentManagers = [], [], []
    
    def advance(self):
        for player in self.players:
            player.advance()
    
    def populateActivePlayerPool(self, n):
        while len(self.activePlayers) < n:
            self.createPlayer()
    
    def createPlayer(self, player = None):
        self.playersCreated += 1
        player = Player(self, id = copy.copy(self.playersCreated)) if player is None else player
        self.players.append(player)
        if player.retired is False:
            self.activePlayers.append(player)
            self.freeAgentPlayers.append(player)
        return player
    
    def populateActiveManagerPool(self, n):
        while len(self.activeManagers) < n:
            self.createManager()

    def createManager(self, manager = None):
        self.managersCreated += 1
        manager = Manager(self, id = copy.copy(self.managersCreated)) if manager is None else manager
        self.managers.append(manager)
        if manager.retired is False:
            self.activeManagers.append(manager)
            self.freeAgentManagers.append(manager)
        else:
            self.retiredManagers.append(manager)
        return manager
    
    def getPlayerById(self, id):
        for player in self.players:
            if player.id == id:
                return player
        return None
                    
_instance = None

def PersonController(universe = None):
    global _instance
    if _instance is None:
        _instance = _PersonController(universe)
    return _instance