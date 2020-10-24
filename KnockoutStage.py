from Fixture import Fixture
from TwoLegKnockoutMatchContainer import TwoLegKnockoutMatchContainer
import random

class KnockoutStage:
    def __init__(self, tournament, stage):
        self.tournament = tournament
        self.stage = stage
        if self.stage == 'final':
            self.fixture = Fixture(self.tournament)
        else:
            if self.stage == 'semiFinals':
                numClubsInStage = 4
            elif self.stage == 'quarterFinals':
                numClubsInStage = 8
            else:
                numClubsInStage = int(self.stage[7:])
            self.initialiseEmptyTwoLegKnockouts(int(numClubsInStage / 2))
        self.complete = False
    
    def initialiseEmptyTwoLegKnockouts(self, n):
        self.firstLegs, self.secondLegs, self.ties = [], [], []
        for i in range(n):
            firstLeg, secondLeg = Fixture(self.tournament), Fixture(self.tournament)
            self.firstLegs.append(firstLeg)
            self.secondLegs.append(secondLeg)
            self.ties.append(TwoLegKnockoutMatchContainer([firstLeg, secondLeg]))
    
    def draw(self, clubs):
        for i in range(int(len(clubs) / 2)):
            pot = clubs
            random.shuffle(pot)
            clubX, clubY = pot.pop(), pot.pop()
            if self.stage == 'final':
                self.fixture.addClubs(clubX, clubY)
            else:
                self.ties[i].fixtures['firstLeg'].addClubs(clubX, clubY) ### First leg
                self.ties[i].fixtures['secondLeg'].addClubs(clubY, clubX) ### Second leg

    def checkNewlyComplete(self):
        if self.stage == 'final':
            if self.complete == False and self.fixture.played == True:
                self.complete = True
                return True
        else:
            if self.complete == False and all([tie.checkComplete() for tie in self.ties]):
                self.complete = True
                return True
        
    def setProgressors(self):
        self.progressors = []
        for tie in self.ties:
            self.progressors.append(tie.returnProgressor())