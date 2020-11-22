import sys
sys.path.append('.')
from Persons.Units.Person import Person

class Physiotherapist(Person):
    def __init__(
        self,
        controller,
        id,
        config = None,
        name = None
        ):
        super(Physiotherapist, self).__init__(controller, id, config, name)
        self.setAttributes()
    
    def setAttributes(self):
        self.attributes = {}
        self.attributes['physiotherapy'] = 1