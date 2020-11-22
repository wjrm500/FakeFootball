import sys
sys.path.append('.')
import Utilities.Utils as Utils
from config import systemConfig
from Persons.Controllers.Subcontrollers.ManagerController import ManagerController
from Persons.Controllers.Subcontrollers.NegotiatorController import NegotiatorController
from Persons.Controllers.Subcontrollers.PhysiotherapistController import PhysiotherapistController
from Persons.Controllers.Subcontrollers.PlayerController import PlayerController
from Persons.Controllers.Subcontrollers.ScoutController import ScoutController
import random
import numpy as np
from Database import Database
import re
import pickle
import copy
from datetime import datetime, timedelta

class Club:
    def __init__(self, system, name, manager = None, squad = None):
        self.system = system
        self.universe = system.universe
        self.name = name
        self.transferBudget = 0
    
    def getProvisionalShortName(self, precedence = 0):
        ### If precedence = 0, use all available consonants
        ### If precedence = 1, ignore third consonant
        ### If precedence = 2, ignore third and fourth consonants
        ### Etc.
        firstLetterAndConsonantsOnly = self.name[0] + re.sub('(?i)[aeiou -\.,]', '', self.name[1:])
        provisionalShortName = (firstLetterAndConsonantsOnly[:precedence + 3] if len(firstLetterAndConsonantsOnly) >= precedence + 3 else self.name[:3]).upper()
        provisionalShortName = provisionalShortName[:2] + provisionalShortName[-1:]
        return provisionalShortName

    def getShortName(self):
        ### Need to ensure no short name clashes with clubs in same league
        ### Basic idea is that clubs with higher ratings receive higher precedence when it comes to "naming rights"
        ### So we find all clubs in league whose provisional short names clash initially
        ### Then we see where this particular club ranks amongst this set of clashing clubs
        ### We then feed this rank as the argument to precedence in the getProvisionalShortName method
        shortName = self.getProvisionalShortName()
        clashingClubs = []
        for club in self.league.clubs:
            if shortName == club.getProvisionalShortName():
                clashingClubs.append(club)
        selfRankAmongClashingClubs = sorted(clashingClubs, key = lambda x: x.getRating(), reverse = True).index(self)
        return self.getProvisionalShortName(precedence = selfRankAmongClashingClubs)
    
    def setLeague(self, league):
        self.league = league
    
    def addPersonnel(self):
        personnelRequired = self.universe.config['numPersonnelPerClub']
        for personnelType, personnelNumber in personnelRequired.items():
            controllerName = personnelType + 'Controller'
            controller = globals()[controllerName]()
            if personnelNumber == 1:
                freeAgent = controller.getRandomFreeAgent()
                freeAgent.club = self
                setattr(self, personnelType.lower(), freeAgent)
            else:
                attributeName = personnelType.lower() + 's'
                setattr(self, attributeName, [])
                for i in range(personnelNumber):
                    freeAgent = controller.getRandomFreeAgent()
                    freeAgent.club = self
                    getattr(self, attributeName).append(freeAgent)
        self.squad = self.players
        delattr(self, 'players')
    
    def getRating(self, decimalPlaces = 2):
        return round(np.mean([player.rating for player in self.squad]), decimalPlaces)
    
    def getPlayersSortedByRating(self):
        squadCopy = self.squad.copy()
        squadCopy.sort(key = lambda x: x.rating, reverse = True)
        return squadCopy
    
    def displayPerformanceIndices(self):
        comp1 = self.league
        comp2 = self.system.systemKnockout
        comp3 = self.system.universe.superiorUniversalTournament
        comp4 = self.system.universe.inferiorUniversalTournament
        competitions = [comp1, comp2, comp3, comp4]
        shortenedCompNames = '{:^23} {:^23} {:^23} {:^23} {:^23}'.format('League', 'System Knockout', 'Superior Universal', 'Inferior Universal', 'Total')
        print('{}{}'.format(' ' * 47, shortenedCompNames))
        print('-' * 163)
        subHeading = 'GP /  G /  A /   PI'
        subHeadings = '{:^23} {:^23} {:^23} {:^23} {:^23}'.format(subHeading, subHeading, subHeading, subHeading, subHeading)
        print('{}{}'.format(' ' * 46, subHeadings))
        print('-' * 163)
        for player in self.getPlayersSortedByRating():
            player.displayOneLinePerformanceIndices(competitions)

    def addProspectivePlayer(self, prospectivePlayer):
        self.squad.append(prospectivePlayer)

    def removeProspectivePlayer(self, prospectivePlayer):
        self.squad.remove(prospectivePlayer)
    
    def getFirstTeam(self):
        return self.manager.selectTeam()
    
    def prepareFeaturesForGetting(self):
        features = {}

        ### Get strength
        firstTeam = self.getFirstTeam()
        features['strength'] = firstTeam.rating

        ### Get depth
        firstTeamPlayers = [select.player for select in firstTeam.selection]
        squadMinusFirstTeamPlayers = [player for player in self.squad if player not in firstTeamPlayers]
        secondTeam = self.manager.selectTeam(squad = squadMinusFirstTeamPlayers)
        features['depth'] = secondTeam.rating / firstTeam.rating

        self.features = features

    def getFeatures(self):
        features = {}

        ### Get strength
        firstTeam = self.getFirstTeam()
        features['strength'] = firstTeam.rating
        features['strength'] /= self.league.getFeature('meanStrength')

        ### Get depth
        firstTeamPlayers = [select.player for select in firstTeam.selection]
        squadMinusFirstTeamPlayers = [player for player in self.squad if player not in firstTeamPlayers]
        secondTeam = self.manager.selectTeam(squad = squadMinusFirstTeamPlayers)
        features['depth'] = secondTeam.rating / firstTeam.rating
        features['depth'] /= self.league.getFeature('meanDepth')

        return features

    def setInternalScoutReports(self):
        self.internalScoutReports = self.scout.getInternalScoutReports()
    
    def setExternalScoutReports(self):
        self.externalScoutReports = self.scout.getExternalScoutReports()