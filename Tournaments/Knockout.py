import sys
sys.path.append('.')
from Tournaments.Tournament import Tournament

class Knockout(Tournament):
    def __init__(self, system):
        super().__init__(system)
    
    def checkAdvance(self):
        for stage in self.stages:
            stageNewlyComplete = stage.checkNewlyComplete()
            stageNotFinal = stage.stage != 'Final'
            if stageNewlyComplete and stageNotFinal:
                self.advanceStages(stage, self.stages[self.stages.index(stage) + 1])

    def advanceStages(self, previousStage, nextStage):
        previousStage.setProgressors()
        if previousStage.stage == 'Preliminary Stage':
            nextStage.draw(previousStage.progressors + self.nonPreliminaryClubs)
        elif previousStage.stage == 'Group Stage':
            if type(self).__name__ == 'SuperiorUniversalTournament':
                nextStage.draw(previousStage.progressors, drawType = 'firstVsSecond')
                previousStage.setDropouts()
            elif type(self).__name__ == 'InferiorUniversalTournament':
                nextStage.draw(previousStage.progressors + self.universe.superiorUniversalTournament.dropouts)
        else:
            nextStage.draw(previousStage.progressors)

    def displayResults(self):       
        for stage in self.stages:
            print(stage.stage)
            print('----------')
            if stage.stage == 'Group Stage':
                for group in stage.groups.values():
                    group.displayLeagueTable()
            elif stage.stage == 'Final':
                clubX = stage.fixture.clubX
                clubY = stage.fixture.clubY
                clubXGoals = stage.fixture.goals[clubX]
                clubYGoals = stage.fixture.goals[clubY]
                print('{:20} {} {:20}'.format(
                    clubX.name,
                    str(clubXGoals) + '-' + str(clubYGoals),
                    clubY.name
                ))
            else:
                for tie in stage.ties:
                    clubX = tie.fixtures['firstLeg'].clubX
                    clubY = tie.fixtures['firstLeg'].clubY
                    clubX1stLegGoals = tie.fixtures['firstLeg'].goals[clubX]
                    clubY1stLegGoals = tie.fixtures['firstLeg'].goals[clubY]
                    clubX2ndLegGoals = tie.fixtures['secondLeg'].goals[clubX]
                    clubY2ndLegGoals = tie.fixtures['secondLeg'].goals[clubY]
                    print('{:20} {} ({}) {} {:20}'.format(
                    clubX.name,
                    str(clubX1stLegGoals) + '-' + str(clubY1stLegGoals),
                    str(clubX1stLegGoals + clubX2ndLegGoals) + '-' + str(clubY1stLegGoals + clubY2ndLegGoals),
                    str(clubX2ndLegGoals) + '-' + str(clubY2ndLegGoals),
                    clubY.name
                    ))
            print('\n')