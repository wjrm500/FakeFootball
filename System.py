import Utilities.Utils as Utils
from Tournaments.SystemKnockout import SystemKnockout
import copy
from Tournaments.League import League
from Club import Club

class System:
    def __init__(self, universe, name = None):
        self.universe = universe
        self.name = Utils.generateName(4) if name is None else name
        self.tournaments = []
    
    def addLeagues(self):
        self.leagues = [League(self, i + 1) for i in range(self.universe.config['numLeaguesPerSystem'])]
        self.tournaments += self.leagues
    
    def addSystemKnockout(self):
        self.systemKnockout = SystemKnockout(self)
        self.tournaments += [self.systemKnockout]
    
    def addClubs(self):
        self.clubs = [Club() for _ in range(self.universe.config['numLeaguesPerSystem'] * self.universe.config['numClubsPerLeague'])]
        
    def populateLeaguesWithClubs(self):
        clubsForPopping = copy.copy(self.clubs)
        for league in self.leagues:
            league.populateWithClubs([clubsForPopping.pop(0) for i in range(self.universe.config['numClubsPerLeague'])])