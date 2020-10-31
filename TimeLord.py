from Universe import Universe
from config import systemConfig
import datetime
import copy
import Utilities.Utils as Utils

class TimeLord:
    def __init__(self, config = None, creationDate = None):
        self.config = copy.deepcopy(systemConfig)
        if config is not None and config != systemConfig:
            Utils.updateConfig(self.config, config)
        if creationDate is not None and type(creationDate) == datetime.date:
            self.creationDate = creationDate
        else:
            self.creationDate = datetime.date(datetime.datetime.now().year, 1, 1)
        self.currentDate = self.creationDate
    
    def getDaysSinceCreation(self):
        delta = self.currentDate - self.creationDate
        return delta.days

    def createUniverse(self):
        self.universe = Universe(self)
        self.universe.populate()
    
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