from Fixture import Fixture
from Tie import Tie
import random
from TournamentStage import TournamentStage

class KnockoutStage(TournamentStage):
    def __init__(self, tournament, stage):
        super().__init__(tournament, stage)
        if self.stage == 'Final':
            self.fixture = Fixture(self.tournament)
        else:
            if self.stage == 'Semi Finals':
                numClubsInStage = 4
            elif self.stage == 'Quarter Finals':
                numClubsInStage = 8
            elif self.stage == 'Preliminary Stage':
                numClubsInStage = self.tournament.numClubsInPreliminaryStage
            else:
                numClubsInStage = int(self.stage[9:])
            self.initialiseEmptyTies(int(numClubsInStage / 2))
    
    def initialiseEmptyTies(self, n):
        self.firstLegs, self.secondLegs, self.ties = [], [], []
        for i in range(n):
            firstLeg, secondLeg = Fixture(self.tournament), Fixture(self.tournament)
            self.firstLegs.append(firstLeg)
            self.secondLegs.append(secondLeg)
            self.ties.append(Tie([firstLeg, secondLeg]))
    
    def draw(self, pot, drawType = 'normal'):
        numClubs = sum([len(value) for value in pot.values()]) if type(pot) == dict else len(pot)
        if drawType == 'normal':
            random.shuffle(pot)
        elif drawType == 'firstVsSecond':
            for weePot in [pot['firsts'], pot['seconds']]:
                random.shuffle(weePot)
        for i in range(int(numClubs / 2)):
            clubX = pot['firsts'].pop() if drawType == 'firstVsSecond' else pot.pop()
            clubY = pot['seconds'].pop() if drawType == 'firstVsSecond' else pot.pop()
            if self.stage == 'Final':
                self.fixture.addClubs(clubX, clubY)
            else:
                self.ties[i].fixtures['firstLeg'].addClubs(clubX, clubY) ### First leg
                self.ties[i].fixtures['secondLeg'].addClubs(clubY, clubX) ### Second leg

    def checkNewlyComplete(self):
        if self.stage == 'Final':
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