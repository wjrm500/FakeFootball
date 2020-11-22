import sys
sys.path.append('.')
from Persons.Units.Person import Person

class Negotiator(Person):
    def __init__(
        self,
        controller,
        id,
        config = None,
        name = None
        ):
        super(Negotiator, self).__init__(controller, id, config, name)
        self.setAttributes()
    
    def setAttributes(self):
        self.attributes = {}
        self.attributes['negotiation'] = 1
    
    def submitInitialBid(self, player, externalValuation):
        self.bids[player] = externalValuation