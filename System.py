from Division import Division
import Utils

class System:
    def __init__(self, systemConfig, name = ""):
        self.divisions = [Division(systemConfig) for _ in range(systemConfig['numDivisionsPerSystem'])]
        self.name = Utils.generateName(name, 4)