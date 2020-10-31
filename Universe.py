from System import System
from config import systemConfig
import Utilities.Utils as Utils
import copy
from PersonController import PersonController
import numpy as np
from Database import Database
from universal_tournament_qualification import universalTournamentQualification
from Tournaments.SuperiorUniversalTournament import SuperiorUniversalTournament
from Tournaments.InferiorUniversalTournament import InferiorUniversalTournament
from Scheduler import Scheduler

class _Universe:
    def __init__(self, timeLord):
        self.timeLord = timeLord
        self.config = timeLord.config
        self.personController = PersonController(self)
        self.systems = []
        self.numSystems = 0
    
    def populate(self):
        db = Database.getInstance()
        db.cursor.execute('SELECT `system_id` FROM `system` ORDER BY RAND() LIMIT {}'.format(self.config['numSystems']))
        systemIds = [row['system_id'] for row in db.cursor.fetchall()]
        for systemId in systemIds:
            self.addSystem(systemId)
        self.personController.populateActiveManagerPool(np.product(list(self.config.values())[:-1]))
        self.personController.populateActivePlayerPool(np.product(list(self.config.values())))
        self.initialiseSystemTournaments()
        self.initialiseUniversalTournaments()
        
    def addSystem(self, systemId):
        newSystem = System(self, systemId)
        self.systems.append(newSystem)
        self.numSystems += 1
    
    def removeSystem(self, name):
        del self.systems[name]
        self.numSystems -= 1
    
    def sortSystems(self):
        if self.timeLord.getDaysSinceCreation() / 365.25 < 5:
            self.systems.sort(key = lambda x: x.getRating(), reverse = True)
        else:
            ### TODO: Something to do with coefficients based on past performance in Universal Tournaments
            pass
    
    def initialiseSystemTournaments(self):
        for system in self.systems:
            system.addLeagues()
            system.addSystemKnockout()
            system.addClubs()
            for club in system.clubs:
                club.addFreeAgentManager()
                club.populateSquad()
            system.populateLeaguesWithClubs()
            system.systemKnockout.populateWithClubs()
            system.systemKnockout.setStages()
            for tournament in system.tournaments:
                Scheduler.scheduleFixtures(self.timeLord.currentDate.year, tournament)
    
    def initialiseUniversalTournaments(self):
        self.tournaments = []
        if self.numSystems >= 6:
            self.superiorUniversalTournament = SuperiorUniversalTournament(self)
            self.tournaments.append(self.superiorUniversalTournament)
        if self.numSystems >= 12:
            self.inferiorUniversalTournament = InferiorUniversalTournament(self)
            self.tournaments.append(self.inferiorUniversalTournament)
        self.populateUniversalTournaments()
        self.stageUniversalTournaments()
        self.scheduleUniversalTournaments()
        self.populateUniversalTournamentsFirstStages()

    def populateUniversalTournaments(self):
        if self.numSystems >= 6:
            self.sortSystems()
            utq = universalTournamentQualification[self.numSystems]
            sutAClubs, sutPOClubs, iutAClubs, iutPOClubs = [], [], [], []
            for system in self.systems:
                systemRanking = self.systems.index(system) + 1
                qualifiers = utq[systemRanking]
                if qualifiers.get('SUT-A') is not None:
                    for tablePosition in qualifiers['SUT-A']:
                        sutAClubs.append(system.clubs[tablePosition - 1])
                if qualifiers.get('SUT-PO') is not None:
                    for tablePosition in qualifiers['SUT-PO']:
                        sutPOClubs.append(system.clubs[tablePosition - 1])
                if qualifiers.get('IUT-A') is not None:
                    for tablePosition in qualifiers['IUT-A']:
                        iutAClubs.append(system.clubs[tablePosition - 1])
                if qualifiers.get('IUT-PO') is not None:
                    for tablePosition in qualifiers['IUT-PO']:
                        iutPOClubs.append(system.clubs[tablePosition - 1])
            if sutAClubs:
                self.superiorUniversalTournament.populateWithClubs(sutAClubs)
            if sutPOClubs:
                self.superiorUniversalTournament.populateWithPreliminaryClubs(sutPOClubs)
            if iutAClubs:
                self.inferiorUniversalTournament.populateWithClubs(iutAClubs)
            if iutPOClubs:
                self.inferiorUniversalTournament.populateWithPreliminaryClubs(iutPOClubs)

    def stageUniversalTournaments(self):
        if hasattr(self, 'superiorUniversalTournament'):
            self.superiorUniversalTournament.setStages()
        if hasattr(self, 'inferiorUniversalTournament'):
            self.inferiorUniversalTournament.setStages()
    
    def scheduleUniversalTournaments(self):
        if hasattr(self, 'superiorUniversalTournament'):
            Scheduler.scheduleFixtures(self.timeLord.currentDate.year, self.superiorUniversalTournament)
        if hasattr(self, 'inferiorUniversalTournament'):
            Scheduler.scheduleFixtures(self.timeLord.currentDate.year, self.inferiorUniversalTournament)
    
    def populateUniversalTournamentsFirstStages(self):
        if hasattr(self, 'superiorUniversalTournament'):
            self.superiorUniversalTournament.populateFirstStage()
        if hasattr(self, 'inferiorUniversalTournament'):
            self.inferiorUniversalTournament.populateFirstStage()

    def playFixtures(self, date):
        for tournament in self.tournaments:
            tournament.playOutstandingFixtures(date)
        for system in self.systems:
            for tournament in system.tournaments:
                tournament.playOutstandingFixtures(date)
    
    def getClubByName(self, clubName):
        for system in self.systems:
            for club in system.clubs:
                if club.name == clubName:
                    return club

_instance = None

def Universe(timeLord, config = None):
    global _instance
    if _instance is None:
        _instance = _Universe(timeLord)
    return _instance