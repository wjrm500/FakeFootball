import Utils

class Team:
    def __init__(self, name = None):
        self.squad = []
        self.transferBudget = 0
        if name == None:
            self.name = Utils.generateName(name, 8)
    
    def signPlayer(self, player, transferFee = 0):
        self.squad.append(player)
        self.transferBudget -= transferFee