from Persons.Player import Player
from Persons.Manager import Manager
import random
import numpy as np
from datetime import date, timedelta
import copy

class _PersonController:
    def __init__(self, creationYear):
        self.currentDate = date(creationYear, 1, 1)
        self.players, self.playersCreated = [], 0
        self.managers, self.managersCreated = [], 0
    
    def advance(self):
        self.currentDate += timedelta(days = 1)
        for player in self.players:
            player.advance()
    
    def createPlayer(self, player = None):
        self.playersCreated += 1
        player = Player(self, id = copy.copy(self.playersCreated)) if player is None else player
        self.players.append(player)
        return player
    
    def createManager(self, manager = None):
        self.managersCreated += 1
        manager = Manager(self, id = copy.copy(self.managersCreated)) if manager is None else manager
        self.managers.append(manager)
        return manager
    
    def getPlayerById(self, id):
        for player in self.players:
            if player.id == id:
                return player
        return None
                    
_instance = None

def PersonController(creationYear = 1900):
    global _instance
    if _instance is None:
        _instance = _PersonController(creationYear)
    return _instance