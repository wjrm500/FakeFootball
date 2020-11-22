from Persistable import Persistable
import Utilities.Utils as Utils
from Tournaments.SystemKnockout import SystemKnockout
import copy
from Tournaments.League import League
from Club import Club
from Database import Database
import numpy as np

class System:
    def __init__(self, universe, systemId):
        self.universe = universe
        self.id = systemId
        db = Database.getInstance()
        db.cursor.execute('SELECT `system_name` FROM `system` WHERE `system_id` = {}'.format(systemId))
        self.name = [row['system_name'] for row in db.cursor.fetchall()][0]
        self.tournaments = []
    
    def addLeagues(self):
        self.leagues = [League(self, i + 1) for i in range(self.universe.config['numLeaguesPerSystem'])]
        self.tournaments += self.leagues
    
    def addSystemKnockout(self):
        self.systemKnockout = SystemKnockout(self)
        self.tournaments += [self.systemKnockout]
    
    def addClubs(self):
        numClubs = self.universe.config['numLeaguesPerSystem'] * self.universe.config['numClubsPerLeague']
        db = Database.getInstance()
        db.cursor.execute('SELECT `city_name` FROM `city` WHERE `system_id` = {} ORDER BY RAND() LIMIT {}'.format(self.id, numClubs))
        cityNames = [row['city_name'] for row in db.cursor.fetchall()]
        self.clubs = [Club(self, cityName) for cityName in cityNames]
    
    def sortClubsByRating(self):
        self.clubs.sort(key = lambda x: x.getRating(), reverse = True)
        
    def populateLeaguesWithClubs(self):
        self.sortClubsByRating()
        clubsForPopping = copy.copy(self.clubs)
        for league in self.leagues:
            poppedClubs = [clubsForPopping.pop(0) for i in range(self.universe.config['numClubsPerLeague'])]
            league.populateWithClubs(poppedClubs)
            for club in league.clubs:
                club.prepareFeaturesForGetting()

    def getRating(self):
        relevantClubs = self.leagues[0].clubs[:8] ### Only the ratings of the top 8 clubs are relevant for Universal Knockouts
        return np.mean([club.getRating() for club in relevantClubs])
