from schedule import leagueSchedule
from datetime import date, timedelta
import random
from Fixture import Fixture
import copy

class Scheduler:
    @classmethod
    def scheduleFixtures(cls, year, tournament): ### Common interface for various tournaments
        functionName = 'schedule' + type(tournament).__name__ + 'Fixtures'
        function = getattr(cls, functionName)
        return function(year, tournament)

    @classmethod
    def scheduleLeagueFixtures(cls, year, league):
        schedule = cls.roundRobinScheduler(league.clubs, robinType = 'double')
        currentDate = date(year, 1, 1)
        gameweek = 1
        while True:
            if currentDate.year > year or not schedule.get(gameweek): ### Exit loop when year changes / when fixtures have been exhausted
                return
            if currentDate.weekday() == 5:
                for game in schedule[gameweek]:
                    clubX, clubY = game['home'], game['away']
                    cls.scheduleFixture(currentDate, league, clubX, clubY)
                gameweek += 1
            currentDate += timedelta(days = 1) 

    @classmethod
    def scheduleSystemKnockoutFixtures(cls, year, systemKnockout):
        currentDate = date(year, 1, 1)
        gameweek = 1
        alternator = "Off"
        systemKnockout.fixtures = []
        while True:
            if currentDate.year > year or not systemKnockout.schedule.get(gameweek): ### Exit loop when year changes / when fixtures have been exhausted
                return
            if currentDate.weekday() == 2:
                alternator = "Off" if alternator == "On" else "On"
                if alternator == "On":
                    for fixture in systemKnockout.schedule[gameweek]:
                        fixture.setDate(currentDate)
                        systemKnockout.fixtures.append(fixture)
                    gameweek += 1
            currentDate += timedelta(days = 1)

    @classmethod
    def scheduleFixture(cls, date, tournament, clubX, clubY):
        if not hasattr(tournament, 'fixtures'):
            tournament.fixtures = []
        fixture = Fixture(tournament, date, clubX, clubY)
        tournament.fixtures.append(fixture)
    
    @classmethod
    def roundRobinScheduler(cls, clubs, robinType = 'single'):
        numClubs = len(clubs)
        if numClubs % 2 != 0:
            raise Exception('Number of clubs must be even')
        schedule = []
        fixturesPerWeek = int(numClubs / 2)
        maxIndex = fixturesPerWeek - 1
        for i in range(numClubs - 1):
            newGameweek = {}
            if i == 0:
                clubsForPopping = copy.copy(clubs)
                for j in range(fixturesPerWeek):
                    newGameweek[j] = [clubsForPopping.pop(0), clubsForPopping.pop()]
            else:
                lastGameweek = schedule[i - 1]
                for j in range(fixturesPerWeek):
                    if j == 0:
                        clubOne = clubs[0]
                    elif j == 1:
                        clubOne = lastGameweek[0][1]
                    else:
                        clubOne = lastGameweek[j - 1][0]

                    if j != maxIndex:
                        clubTwo = lastGameweek[j + 1][1]
                    else:
                        clubTwo = lastGameweek[maxIndex][0]
                    
                    newGameweek[j] = [clubOne, clubTwo]
            schedule.append(newGameweek)
        
        for i, gameweek in enumerate(schedule):
            if i % 2 != 0: ### If index is odd - to only flip teams on alternate gameweeks
                for key, value in gameweek.items():
                    gameweek[key] = [value[1], value[0]] ### Flip home and away teams
        
        if robinType == 'double': ### If double round-robin
            flippedSchedule = copy.deepcopy(schedule)
            for i, gameweek in enumerate(flippedSchedule):
                for key, value in gameweek.items():
                    gameweek[key] = [value[1], value[0]] ### Flip home and away teams
            schedule = schedule + flippedSchedule

        reformattedSchedule = {}
        for i, gameweek in enumerate(schedule):
            fixtureList = [{'home': value[0], 'away': value[1]} for value in gameweek.values()]
            reformattedSchedule[i + 1] = fixtureList

        return reformattedSchedule