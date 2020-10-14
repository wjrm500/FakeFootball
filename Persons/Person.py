import sys
sys.path.append('.')
import Utilities.Utils as Utils
from config import playerConfig, managerConfig
import random

class Person:
    def __init__(self, personController, id, name = None, age = None):
        self.personController = personController
        self.id = id
        self.setName(name)
        self.setBirthDate(age)
        self.setAge()
    
    def __str__(self):
        return '< ' + self.__class__.__name__ + ' | ' + self.properName + ' >'
    
    def setName(self, name):
        self.name = Utils.generatePlayerName() if name is None else name
        self.properName = ' '.join(self.name)
    
    def setBirthDate(self, age):
        if age is None:
            agMin, agMax = playerConfig['age']['min'], playerConfig['age']['max']
            age = random.randint(agMin, agMax)
        self.birthDate = Utils.getBirthDate(self.personController.currentDate, age)
    
    def setAge(self):
        td = self.personController.currentDate - self.birthDate
        self.age = td.days / 365.25
    
    def advance(self):
        self.setAge()