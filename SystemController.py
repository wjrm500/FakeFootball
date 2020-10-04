from System import System
from schedule import schedule
from datetime import date, timedelta
from config import systemConfig

class _SystemController:
    def __init__(self):
        self.systemConfig = systemConfig
        self.systems = []
        self.schedule = schedule
    
    def initialise(self):
        for _ in range(self.systemConfig['numSystems']):
            self.addSystem()
    
    def addSystem(self, name = None):
        self.systems.append(System(self.systemConfig, name))
    
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
                        division.playFixture(fixture)


_instance = None

def SystemController():
    global _instance
    if _instance is None:
        _instance = _SystemController()
    return _instance