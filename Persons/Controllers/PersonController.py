import copy
import random

class PersonController:
    def __init__(self, universe):
        self.universe = universe
        self.units, self.unitsCreated = [], 0
        self.activeUnits, self.retiredUnits, self.freeAgentUnits = [], [], []

    def getUnitById(self, id):
        for unit in self.units:
            if unit.id == id:
                return unit
        return None
    
    def getUnitsByName(self, name):
        units = []
        for unit in self.units:
            if unit.name == name:
                units.append(unit)
        return units
    
    def advance(self):
        for unit in self.units:
            unit.advance()
    
    def populateActiveUnitPool(self, n):
        while len(self.activeUnits) < n:
            self.createUnit()
    
    def createUnit(self, object, unit = None):
        self.unitsCreated += 1
        unit = object(self, id = copy.copy(self.unitsCreated)) if unit is None else unit
        self.units.append(unit)
        if hasattr(unit, 'retired') and unit.retired is False:
            self.activeUnits.append(unit)
            self.freeAgentUnits.append(unit)
        return unit

    def getRandomFreeAgent(self):
        return self.freeAgentUnits.pop(random.randrange(len(self.freeAgentUnits)))
    
    def retireUnit(self, unit):
        if not unit in self.activeUnits:
            return 'Unit not active'
        self.activeUnits.remove(unit)
        self.retiredUnits.append(unit)