import sys
sys.path.append('.')
from Persons.Controllers.PersonController import PersonController
from Persons.Units.Subunits.Negotiator import Negotiator

class _NegotiatorController(PersonController):
    def __init__(self, universe):
        super().__init__(universe)
        self.role = 'Negotiator'
    
    def createUnit(self):
        super().createUnit(Negotiator)

_instance = None

def NegotiatorController(universe = None):
    global _instance
    if _instance is None:
        _instance = _NegotiatorController(universe)
    return _instance