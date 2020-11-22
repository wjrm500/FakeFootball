import sys
sys.path.append('.')
from Persons.Controllers.PersonController import PersonController
from Persons.Units.Subunits.Player import Player

class _PlayerController(PersonController):
    def __init__(self, universe):
        super().__init__(universe)
        self.role = 'Player'
    
    def createUnit(self):
        super().createUnit(Player)

_instance = None

def PlayerController(universe = None):
    global _instance
    if _instance is None:
        _instance = _PlayerController(universe)
    return _instance