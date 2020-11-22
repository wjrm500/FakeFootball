import sys
sys.path.append('.')
from Persons.Controllers.PersonController import PersonController
from Persons.Units.Subunits.Scout import Scout

class _ScoutController(PersonController):
    def __init__(self, universe):
        super().__init__(universe)
        self.role = 'Scout'

    def createUnit(self):
        super().createUnit(Scout)

_instance = None

def ScoutController(universe = None):
    global _instance
    if _instance is None:
        _instance = _ScoutController(universe)
    return _instance