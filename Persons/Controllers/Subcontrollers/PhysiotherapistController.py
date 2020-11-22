import sys
sys.path.append('.')
from Persons.Controllers.PersonController import PersonController
from Persons.Units.Subunits.Physiotherapist import Physiotherapist

class _PhysiotherapistController(PersonController):
    def __init__(self, universe):
        super().__init__(universe)
        self.role = 'Physiotherapist'
    
    def createUnit(self):
        super().createUnit(Physiotherapist)

_instance = None

def PhysiotherapistController(universe = None):
    global _instance
    if _instance is None:
        _instance = _PhysiotherapistController(universe)
    return _instance