import sys
sys.path.append('.')
import Utilities.Utils as Utils
from config import personConfig
import random
import copy

class Person:
    def __init__(self, controller, id, config, name = None, age = None):
        self.controller = controller
        self.creationDate = self.controller.universe.timeLord.currentDate
        self.id = id
        self.setConfig(config)
        self.setName(name)
        self.setBirthDate(age)
        self.setAge()
        self.retired = False
        self.club = None
    
    def __str__(self):
        return '< ' + self.__class__.__name__ + ' | ' + self.properName + ' >'

    def setConfig(self, config):
        self.config = copy.deepcopy(personConfig[self.__class__.__name__.lower()])
        if config is not None:
            Utils.updateConfig(self.config, config)

    def getProperName(self, forenameStyle = 'Whole', surnameStyle = 'Whole'):
        ### Both forenameStyle and surnameStyle arguments can be set to either 'Empty', 'Shortened' or 'Whole'
        forename, surname = self.name[0], self.name[1]
        properNameArray = []
        for style, name in zip([forenameStyle, surnameStyle], [forename, surname]):
            if style == 'Shortened':
                properNameArray.append(name[0] + '.')
            elif style == 'Whole':
                properNameArray.append(name)
        return ' '.join(properNameArray)

    def setName(self, name):
        self.name = Utils.generatePlayerName() if name is None else name
        self.properName = self.getProperName()

    def setBirthDate(self, age):
        if age is None:
            agMin, agMax = self.config['age']['min'], self.config['age']['max']
            age = random.randint(agMin, agMax)
        self.birthDate = Utils.getBirthDate(self.creationDate, age)
    
    def setAge(self):
        td = self.creationDate - self.birthDate
        self.age = td.days / 365.25
    
    def advance(self):
        self.setAge()