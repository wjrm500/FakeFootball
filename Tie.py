import random

class Tie:
    def __init__(self, fixtures):
        self.fixtures = {
            'firstLeg': fixtures[0],
            'secondLeg': fixtures[1]
        }
        self.progressor = None
    
    def checkComplete(self):
        return all([fixture.played for fixture in self.fixtures.values()])
    
    def returnProgressor(self):
        clubX, clubY = self.fixtures['firstLeg'].goals.keys()
        clubXAggregateGoals = self.fixtures['firstLeg'].goals[clubX] + self.fixtures['secondLeg'].goals[clubX]
        clubYAggregateGoals = self.fixtures['firstLeg'].goals[clubY] + self.fixtures['secondLeg'].goals[clubY]
        if clubXAggregateGoals > clubYAggregateGoals:
            self.progressor = clubX
        elif clubYAggregateGoals > clubXAggregateGoals:
            self.progressor = clubY
        else:
            clubXAwayGoals = self.fixtures['secondLeg'].goals[clubX]
            clubYAwayGoals = self.fixtures['firstLeg'].goals[clubY]
            if clubXAwayGoals > clubYAwayGoals:
                self.progressor = clubX
            elif clubYAwayGoals > clubXAwayGoals:
                self.progressor = clubY
            else:
                self.progressor = random.choice([clubX, clubY])
        return self.progressor