from Persons.Player import Player
from Persons.Manager import Manager
import random
import numpy as np
from datetime import date, timedelta

class _PersonController:
    def __init__(self, creationYear):
        self.currentDate = date(creationYear, 1, 1)
        self.players = []
        self.managers = []
    
    def advance(self):
        self.currentDate += timedelta(days = 1)
        for player in self.players:
            player.advance()
    
    def createPlayer(self, player = None):
        player = Player(self) if player is None else player
        self.players.append(player)
        return player
    
    def createManager(self, manager = None):
        manager = Manager(self) if manager is None else manager
        self.managers.append(manager)
        return manager
                    
_instance = None

def PersonController(creationYear = 1900):
    global _instance
    if _instance is None:
        _instance = _PersonController(creationYear)
    return _instance