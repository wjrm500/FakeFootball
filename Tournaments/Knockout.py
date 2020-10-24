import sys
sys.path.append('.')
from Tournaments.Tournament import Tournament

class Knockout(Tournament):
    def __init__(self, system):
        super().__init__(system)
    
    def checkAdvance(self):
        for stage in self.stages:
            stageNewlyComplete = stage.checkNewlyComplete()
            stageNotFinal = stage.stage != 'final'
            if stageNewlyComplete and stageNotFinal:
                self.advanceStages(stage, self.stages[self.stages.index(stage) + 1])

    def advanceStages(self, previousStage, nextStage):
        previousStage.setProgressors()
        if previousStage.stage == 'preliminary':
            nextStage.draw(previousStage.progressors + self.nonPrelimClubs)
        else:
            nextStage.draw(previousStage.progressors)