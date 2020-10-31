import sys
sys.path.append('.')
from Tournaments.Knockout import Knockout
from KnockoutStage import KnockoutStage
from Tie import Tie
from Scheduler import Scheduler
import Utilities.Utils as Utils

class SystemKnockout(Knockout):
    def __init__(self, system):
        super().__init__(system)
    
    def __str__(self):
        return '<System Knockout>';

    def populateWithClubs(self):
        super().populateWithClubs([club for league in self.system.leagues for club in league.clubs])

    def setStages(self):
        self.stages = []
        clubsByStages = Utils.getAllPowersOfTwoLessThan(self.numClubs)
        clubsByStages = list(filter(lambda x: x != 1, clubsByStages))
        for clubsByStage in clubsByStages:
            if clubsByStage == 2:
                stageName = 'Final'
            elif clubsByStage == 4:
                stageName = 'Semi Finals'
            elif clubsByStage == 8:
                stageName = 'Quarter Finals'
            else:
                stageName = 'Round of {}'.format(clubsByStage)
            self.stages.append(KnockoutStage(self, stageName))
        if self.numClubs not in clubsByStages: ### Is preliminary stage necessary?
            numClubsToEliminateInPreliminary = self.numClubs - max(clubsByStages)
            self.numClubsInPreliminaryStage = numClubsToEliminateInPreliminary * 2
            self.stages.insert(0, KnockoutStage(self, 'Preliminary Stage'))
            self.populatePreliminaryStage()
        else:
            self.stages[0].draw(self.clubs.copy())
        i = 1
        self.schedule = {}
        for stage in self.stages:
            if stage.stage == 'Final':
                self.schedule[i] = [stage.fixture]
            else:
                for legs in [stage.firstLegs, stage.secondLegs]:
                    self.schedule[i] = legs
                    i += 1
    
    def populatePreliminaryStage(self):
        numClubs = self.numClubsInPreliminaryStage
        self.preliminaryClubs = self.clubs[-numClubs:]
        self.nonPreliminaryClubs = self.clubs[:-numClubs]
        self.stages[0].draw(self.preliminaryClubs)