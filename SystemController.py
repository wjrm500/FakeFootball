from System import System

class SystemController:
    def __init__(self, systemConfig):
        self.systemConfig = systemConfig
        self.systems = []
    
    def initialise(self):
        for _ in range(self.systemConfig['numSystems']):
            self.systems.append(System(self.systemConfig))
    
    def getSystems(self):
        return self.systems
    
    def addSystem(self, name):
        self.systems.append({name: System(name)})
    
    def removeSystem(self, name):
        del self.systems[name]
