import sys
sys.path.append('.')
from Tournaments.Knockout import Knockout
from KnockoutStage import KnockoutStage
from TwoLegKnockoutMatchContainer import TwoLegKnockoutMatchContainer
from Scheduler import Scheduler

class GlobalKnockout(Knockout):
    def __init__(self, system):
        super().__init__(system)
        self.stages = [
            LeagueStage(self),
            KnockoutStage(self, 'roundOf16'),
            KnockoutStage(self, 'quarterFinals'),
            KnockoutStage(self, 'semiFinals'),
            KnockoutStage(self, 'final')
        ]
        i = 1
        self.schedule = {}
        for stage in self.stages:
            if stage.stage == 'final':
                self.schedule[i] = [stage.fixture]
            else:
                for legs in [stage.firstLegs, stage.secondLegs]:
                    self.schedule[i] = legs
                    i += 1
    
    def __str__(self):
        return '<National Knockout>';

    def populateWithClubs(self):
        super().populateWithClubs([club for league in self.system.leagues for club in league.clubs])
        self.populatePreliminaryStage()
    
    def populatePreliminaryStage(self):
        self.prelimClubs = self.clubs[-32:]
        self.nonPrelimClubs = self.clubs[:-32]
        self.stages[0].draw(self.prelimClubs)