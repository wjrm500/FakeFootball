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
    def scheduleLeagueFixtures(cls, year, league, weekday = 5):
        schedule = cls.roundRobinScheduler(league, robinType = 'double')
        currentDate = date(year, 1, 1)
        gameweek = 1
        while True:
            if currentDate.year > year or not schedule.get(gameweek): ### Exit loop when year changes / when fixtures have been exhausted
                return
            if currentDate.weekday() == weekday:
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
    def scheduleSuperiorUniversalTournamentFixtures(cls, year, universalTournament):
        ##################################################
        # Building schedule
        ##################################################

        ### Preliminary stage schedule

        universalTournament.schedule = {}
        gameweek = 1
        if universalTournament.includesPreliminaryStage:
            preliminaryStage = universalTournament.stages[0]
            for legs in [stage.firstLegs, stage.secondLegs]:
                universalTournament.schedule[i] = legs
                gameweek += 1

        ### Group stage schedule

        groupStageSchedules = []
        groupStageIndex = 1 if universalTournament.includesPreliminaryStage else 0
        for group in universalTournament.stages[groupStageIndex].groups.values():
            groupStageSchedule = cls.roundRobinScheduler(group, robinType = 'double', returnedObject = 'fixture')
            group.fixtures = [fixture for value in groupStageSchedule.values() for fixture in value]
            groupStageSchedules.append(groupStageSchedule)
        combinedGroupStageSchedule = {j: [] for j in range(gameweek, gameweek + 6)}
        for idx, key in enumerate(combinedGroupStageSchedule.keys()):
            singleGameweekGroupStageSchedules = [groupStageSchedule[idx + 1] for groupStageSchedule in groupStageSchedules]
            for singleGameweekGroupStageSchedule in singleGameweekGroupStageSchedules:
                for match in singleGameweekGroupStageSchedule:
                    combinedGroupStageSchedule[key].append(match)
            gameweek += 1
        universalTournament.schedule.update(combinedGroupStageSchedule)

        ### Knockout stages schedule

        knockoutBeginsIndex = 2 if universalTournament.includesPreliminaryStage else 1
        for stage in universalTournament.stages[knockoutBeginsIndex:]:
            if stage.stage == 'Final':
                universalTournament.schedule[gameweek] = [stage.fixture]
            else:
                for legs in [stage.firstLegs, stage.secondLegs]:
                    universalTournament.schedule[gameweek] = legs
                    gameweek += 1
        
        ##################################################
        # Converting schedule to fixtures
        ##################################################

        currentDate = date(year, 1, 1)
        gameweek = 1
        alternator = "On"
        universalTournament.fixtures = []
        while True:
            if currentDate.year > year or not universalTournament.schedule.get(gameweek): ### Exit loop when year changes / when fixtures have been exhausted
                return
            if currentDate.weekday() == 2:
                alternator = "Off" if alternator == "On" else "On"
                if alternator == "On":
                    for fixture in universalTournament.schedule[gameweek]:
                        fixture.setDate(currentDate)
                        universalTournament.fixtures.append(fixture)
                    gameweek += 1
            currentDate += timedelta(days = 1)
    
    @classmethod
    def scheduleInferiorUniversalTournamentFixtures(cls, year, universalTournament):
        cls.scheduleSuperiorUniversalTournamentFixtures(year, universalTournament)

    @classmethod
    def scheduleFixture(cls, date, tournament, clubX, clubY):
        if not hasattr(tournament, 'fixtures'):
            tournament.fixtures = []
        fixture = Fixture(tournament, date, clubX, clubY)
        tournament.fixtures.append(fixture)
    
    @classmethod
    def roundRobinScheduler(cls, tournament, robinType = 'single', returnedObject = 'dict'):
        numClubs = len(tournament.clubs)
        if numClubs % 2 != 0:
            raise Exception('Number of clubs must be even')
        schedule = []
        fixturesPerWeek = int(numClubs / 2)
        maxIndex = fixturesPerWeek - 1
        for i in range(numClubs - 1):
            newGameweek = {}
            if i == 0:
                clubsForPopping = copy.copy(tournament.clubs)
                for j in range(fixturesPerWeek):
                    newGameweek[j] = [clubsForPopping.pop(0), clubsForPopping.pop()]
            else:
                lastGameweek = schedule[i - 1]
                for j in range(fixturesPerWeek):
                    if j == 0:
                        clubOne = tournament.clubs[0]
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
            flippedSchedule = [copy.copy(gameweek) for gameweek in schedule] ### copy.copy(schedule) does not work because the list objects containing clubs in schedule are mutated // copy.deepcopy(schedule) does not work because club objects are duplicated so effectively a separate set of clubs is referenced in second half of schedule
            for i, gameweek in enumerate(flippedSchedule):
                for key, value in gameweek.items():
                    gameweek[key] = [value[1], value[0]] ### Flip home and away teams
            schedule = schedule + flippedSchedule

        reformattedSchedule = {}
        for i, gameweek in enumerate(schedule):
            if returnedObject == 'dict':
                fixtureList = [{'home': value[0], 'away': value[1]} for value in gameweek.values()]
            elif returnedObject == 'fixture':
                fixtureList = [Fixture(tournament, clubX = value[0], clubY = value[1]) for value in gameweek.values()]
            reformattedSchedule[i + 1] = fixtureList

        return reformattedSchedule