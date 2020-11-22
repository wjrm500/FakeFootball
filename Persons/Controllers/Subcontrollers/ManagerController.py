import sys
sys.path.append('.')
from Persons.Controllers.PersonController import PersonController
from Persons.Units.Subunits.Manager import Manager

class _ManagerController(PersonController):
    def __init__(self, universe):
        super().__init__(universe)
        self.role = 'Manager'

    def createUnit(self):
        super().createUnit(Manager)

_instance = None

def ManagerController(universe = None):
    global _instance
    if _instance is None:
        _instance = _ManagerController(universe)
    return _instance