import sys
sys.path.append('.')
from Tournaments.Knockout import Knockout
from GroupStage import GroupStage
from KnockoutStage import KnockoutStage

class InferiorUniversalTournament(Knockout):
    def __init__(self, universe):
        self.universe = universe
        self.includesPreliminaryStage = False
        super().__init__(None)
        
    def populateWithPreliminaryClubs(self, clubs):
        self.preliminaryClubs = []
        for club in clubs:
            self.preliminaryClubs.append(club)
        self.clubs.extend(self.preliminaryClubs)
        self.nonPreliminaryClubs = [club for club in self.clubs if club not in self.preliminaryClubs]

    def setStages(self):
        self.stages = [
            GroupStage(self),
            KnockoutStage(self, 'Round of 32'),
            KnockoutStage(self, 'Round of 16'),
            KnockoutStage(self, 'Quarter Finals'),
            KnockoutStage(self, 'Semi Finals'),
            KnockoutStage(self, 'Final')
        ]
        if len(self.universe.systems) >= 20: ### Is preliminary stage necessary?
            self.includesPreliminaryStage = True
            self.stages.insert(0, KnockoutStage(self, 'Preliminary Stage'))
    
    def populateFirstStage(self):
        if self.includesPreliminaryStage:
            self.stages[0].draw(self.preliminaryClubs)
        else:
            self.stages[0].draw(self.clubs)