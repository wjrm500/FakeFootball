from Player import Player
import random

class PlayerController:
    def __init__(self, playerConfig):
        self.playerConfig = playerConfig
        self.players = {
            'freeAgents': [],
            'signedToTeam': [] 
        }
    
    def addPlayer(self, player = None):
        if player == None:
            player = Player(self.playerConfig)
        self.players['freeAgents'].append(player)
    
    def getRandomFreeAgent(self):
        return random.choice(self.players['freeAgents'])