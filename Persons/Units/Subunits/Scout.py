import sys
sys.path.append('.')
from Persons.Units.Person import Person
import Utilities.Utils as Utils
import random
import copy
import pickle
import numpy as np

class Scout(Person):
    with open('LinearRegression10721', 'rb') as file:
        predictedRankModel = pickle.load(file)

    def __init__(
        self,
        controller,
        id,
        config = None,
        name = None
        ):
        super(Scout, self).__init__(controller, id, config, name)
        self.setAttributes()
    
    def setAttributes(self):
        self.attributes = {}
        for attribute, statsDictionary in self.config['attributes'].items():
            self.attributes[attribute] = Utils.limitedRandNorm(statsDictionary)
    
    def getInternalScoutReports(self):
        internalScoutReports = {}
        squadCopy = copy.copy(self.club.squad)
        for prospectivePlayer in squadCopy: ### Must iterate over a copy to ensure full squad coverage as mutating actual squad in for loop
            internalScoutReports[prospectivePlayer] = self.getInternalValuation(prospectivePlayer)
        return internalScoutReports
    
    def getInternalValuation(self, prospectivePlayer):
        predictedRankModel = self.__class__.predictedRankModel
        self.club.removeProspectivePlayer(prospectivePlayer)
        features = self.club.getFeatures()
        x1 = np.array([list(features.values())])
        predictedRankWithoutPlayer = Utils.limitValue(predictedRankModel.predict(x1)[0], mn = 1, mx = 20)
        predictedRanksWithPlayer = {}
        for yearsIntoFuture in range(1, 11):
            prospectivePlayer.setFutureVersion(yearsIntoFuture)
            self.club.addProspectivePlayer(prospectivePlayer)
            features = self.club.getFeatures()
            x2 = np.array([list(features.values())])
            predictedRanksWithPlayer[yearsIntoFuture] = Utils.limitValue(predictedRankModel.predict(x2)[0], mn = 1, mx = 20)
            self.club.removeProspectivePlayer(prospectivePlayer)
        imperfectValuation, perfectValuation = 0, 0
        judgment = copy.copy(self.attributes['judgment']) * 1.1 ### Judgment higher for internal valuation
        for yearsIntoFuture, predictedRankWithPlayer in predictedRanksWithPlayer.items():
            predictedRankValues = list(map(lambda x: 1 - (np.power(x, (1 / 5)) / 2) * 100_000_000, [predictedRankWithoutPlayer, predictedRankWithPlayer]))
            perfectValueAdded = Utils.limitValue(predictedRankValues[1] - predictedRankValues[0], mn = 0)
            perfectValueAdded *= (1 - (np.power(yearsIntoFuture, (1 / 5)) / 2)) * 2 ### Future tax
            perfectValuation += perfectValueAdded
            imperfectValueAdded = perfectValueAdded * random.uniform(judgment, 2 - judgment) ### Scout's imperfect judgment
            imperfectValuation += imperfectValueAdded
            judgment *= self.attributes['foresight']
        imperfectValuation *= self.attributes['internalBias']
        prospectivePlayer.unsetFutureVersion()
        self.club.addProspectivePlayer(prospectivePlayer)
        return {
            'Imperfect': imperfectValuation,
            'Perfect': perfectValuation
        }

    def getExternalScoutReports(self):
        externalScoutReports = {}
        features = self.club.getFeatures()
        x1 = np.array([list(features.values())])
        predictedRankModel = self.__class__.predictedRankModel
        predictedRankWithoutPlayer = predictedRankModel.predict(x1)[0]
        predictedRankWithoutPlayer = Utils.limitValue(predictedRankWithoutPlayer, mn = 1, mx = 20)
        for system in self.club.universe.systems:
            for club in system.clubs:
                if club is not self:
                    for prospectivePlayer in club.squad:
                        externalValuation = self.getExternalValuation(predictedRankWithoutPlayer, prospectivePlayer)
                        externalScoutReports[prospectivePlayer] = externalValuation
        return externalScoutReports
    
    def getExternalValuation(self, predictedRankWithoutPlayer, prospectivePlayer):
        predictedRankModel = self.__class__.predictedRankModel
        predictedRanksWithPlayer = {}
        for yearsIntoFuture in range(1, 11):
            prospectivePlayer.setFutureVersion(yearsIntoFuture)
            self.club.addProspectivePlayer(prospectivePlayer)
            features = self.club.getFeatures()
            x2 = np.array([list(features.values())])
            predictedRanksWithPlayer[yearsIntoFuture] = predictedRankModel.predict(x2)
            self.club.removeProspectivePlayer(prospectivePlayer)
        imperfectValuation, perfectValuation = 0, 0
        judgment = copy.copy(self.attributes['judgment']) * 0.9 ### Judgment lower for external valuation
        for yearsIntoFuture, predictedRankWithPlayer in predictedRanksWithPlayer.items():
            predictedRankWithPlayer = Utils.limitValue(predictedRankWithPlayer[0], mn = 1, mx = 20)
            predictedRankValues = list(map(lambda x: 1 - (np.power(x, (1 / 5)) / 2) * 100_000_000, [predictedRankWithoutPlayer, predictedRankWithPlayer]))
            perfectValueAdded = Utils.limitValue(predictedRankValues[1] - predictedRankValues[0], mn = 0)
            perfectValueAdded *= (1 - (np.power(yearsIntoFuture, (1 / 5)) / 2)) * 2 ### Future tax
            perfectValuation += perfectValueAdded
            imperfectValueAdded = perfectValueAdded * random.uniform(judgment, 2 - judgment) ### Scout's imperfect judgment
            imperfectValuation += imperfectValueAdded
            judgment *= self.attributes['foresight']
        prospectivePlayer.unsetFutureVersion()
        return {
            'Imperfect': imperfectValuation,
            'Perfect': perfectValuation
        }