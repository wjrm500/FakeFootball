from Universe import Universe
import datetime
from Scheduler import Scheduler

class TimeLord:
    def __init__(self, currentDate = None):
        if currentDate is not None and type(currentDate) == datetime.date:
            self.currentDate = currentDate
        else:
            self.currentDate = datetime.date(datetime.datetime.now().year, 1, 1)

    def createUniverse(self):
        self.universe = Universe(self)
        self.universe.populate()
    
    def scheduleFixtures(self):
        for system in self.universe.systems:
            for tournament in system.tournaments:
                Scheduler.scheduleFixtures(self.currentDate.year, tournament)
    
    def timeTravel(self, days):
        for i in range(days):
            print(i)
            self.resolveQuotidia()
            self.advanceOneDay()
    
    def resolveQuotidia(self):
        self.universe.playFixtures(self.currentDate)
    
    def advanceOneDay(self):
        yearBefore = self.currentDate.year
        self.currentDate += datetime.timedelta(days = 1)
        yearAfter = self.currentDate.year
        if yearBefore != yearAfter:
            self.transitionSeasons(yearBefore, yearAfter)
            return
        self.universe.personController.advance()

    def transitionSeasons(self, oldYear, newYear):
        # ### Persist data
        # ### Promotion and relegation
        # self.Universe.promoteRelegate()
        # ### Qualification for cups
        # ### Schedule fixtures
        self.universe.scheduleFixtures(newYear)
        self.personController.updateYear()
        ### Player retirement
        ### Generate new players to replace retirees
        # ### Transfers
    
    def conductArmageddon(self):
        pass
        ### Persist data
        ### Shut down