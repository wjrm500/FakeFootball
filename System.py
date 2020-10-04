from Division import Division
import Utilities.Utils as Utils

class System:
    def __init__(self, systemConfig, name = None):
        self.name = Utils.generateName(4) if name is None else name
        self.divisions = [Division(self, systemConfig) for _ in range(systemConfig['numDivisionsPerSystem'])]