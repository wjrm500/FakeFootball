import Utilities.Utils as Utils
from Tournaments.NationalKnockout import NationalKnockout

class System:
    def __init__(self, universe, name = None):
        self.universe = universe
        self.name = Utils.generateName(4) if name is None else name
        self.leagues = []
        self.nationalKnockout = NationalKnockout(self)
        self.tournaments = self.leagues + [self.nationalKnockout]
    
    def populateWithLeagues(self, leagues):
        for league in leagues:
            self.leagues.append(league)
            self.tournaments.append(league)