import Utilities.Utils as Utils
from config import systemConfig
from PersonController import PersonController

class Club:
    def __init__(self, division = None, name = None, manager = None, squad = None):
        if division is not None:
            self.system = division.system
            self.division = division
        self.name = Utils.generateName(8) if name is None else name
        self.transferBudget = 0
        self.addManager(manager)
        self.populateSquad(squad)
        
    def populateSquad(self, squad):
        self.squad = []
        if squad is None:
            personController = PersonController()
            while len(self.squad) < systemConfig['numPlayersPerTeam']:
                player = personController.createPlayer()
                if player.retired is False:
                    self.addPlayer(player)
        else:
            for player in squad:
                if player.retired is False:
                    self.addPlayer(player)
    
    def addPlayer(self, player, transferFee = 0):
        self.squad.append(player)
        player.club = self
        self.transferBudget -= transferFee
    
    def addManager(self, manager):
        if manager is None:
            personController = PersonController()
            manager = personController.createManager()
        self.manager = manager
        manager.club = self