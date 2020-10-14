from System import System
from schedule import schedule
from datetime import date, timedelta
from config import systemConfig
import Utilities.Utils as Utils
import copy

class _SystemController:
    def __init__(self, config):
        self.config = copy.deepcopy(systemConfig)
        if config is not None and config != systemConfig:
            Utils.updateConfig(self.config, config)
        self.systems = []
        self.schedule = schedule
    
    def initialise(self):
        for _ in range(self.config['numSystems']):
            self.addSystem()
    
    def addSystem(self, name = None):
        self.systems.append(System(self.config, name))
    
    def removeSystem(self, name):
        del self.systems[name]
    
    def scheduleFixtures(self, year):
        currentDate = date(year, 1, 1)
        endDate = date(year, 12, 31)
        gameweek = 1
        while currentDate <= endDate:
            if not self.schedule.get(gameweek): ### Check whether schedule has been exhausted
                break
            if currentDate.weekday() == 5:
                for system in self.systems:
                    for division in system.divisions:
                        for game in self.schedule[gameweek]:
                            clubX = division.clubs[game['homeSlot']]
                            clubY = division.clubs[game['awaySlot']]
                            division.scheduleFixture(currentDate, clubX, clubY)
                gameweek += 1
            currentDate += timedelta(days = 1)
    
    def playFixtures(self, date):
        for system in self.systems:
            for division in system.divisions:
                if division.schedule.get(date):
                    fixtures = division.schedule[date]
                    for fixture in fixtures:
                        division.playFixture(date, fixture)


_instance = None

def SystemController(config = None):
    global _instance
    if _instance is None:
        _instance = _SystemController(config)
    return _instance