from SystemController import SystemController
from PersonController import PersonController
from datetime import date, timedelta

class TimeLord:
    def __init__(self, creationYear, armageddonYear):
        self.systemController = SystemController()
        self.personController = PersonController()
        self.creationYear = creationYear
        self.armageddonYear = armageddonYear
        self.currentDate = date(creationYear, 1, 1)
        self.armageddonDate = date(armageddonYear, 1, 1)
    
    def createUniverse(self):
        self.systemController.initialise()
        self.systemController.scheduleFixtures(self.creationYear)
    
    def timeTravel(self, days):
        for _ in range(days):
            self.resolveQuotidia()
            self.advanceOneDay()
    
    def resolveQuotidia(self):
        self.systemController.playFixtures(self.currentDate)
    
    def advanceOneDay(self):
        yearBefore = self.currentDate.year
        self.currentDate += timedelta(days = 1)
        yearAfter = self.currentDate.year
        if yearBefore != yearAfter:
            self.transition(yearBefore, yearAfter)

    def transitionSeasons(self, oldYear, newYear):
        pass
        # ### Persist data
        # ### Promotion and relegation
        # self.systemController.promoteRelegate()
        # ### Qualification for cups
        # ### Schedule fixtures
        self.systemController.scheduleFixtures(newYear)
        # ### Transfers
    
    def conductArmageddon(self):
        pass
        ### Persist data
        ### Shut down