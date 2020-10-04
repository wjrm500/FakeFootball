import sys
sys.path.append('.')
from Persons.Person import Person
import Utilities.Utils as Utils
import random
import numpy as np
from scipy import spatial
from config import playerConfig
import copy

class Player(Person):
    def __init__(
        self,
        config = None,
        name = None,
        age = None,
        peakAge = None,
        growthSpeed = None,
        retirementThreshold = None,
        peakRating = None,
        underlyingSkillDistribution = None
        ):
        super(Player, self).__init__(name)
        self.config = copy.deepcopy(playerConfig)
        if config is not None and config != playerConfig:
            Utils.updateConfig(self.config, config)
        self.age = self.setAge() if age is None else age
        self.peakAge = self.setPeakAge() if peakAge is None else peakAge
        self.growthSpeed = self.setGrowthSpeed() if growthSpeed is None else growthSpeed
        self.retirementThreshold = self.setRetirementThreshold() if retirementThreshold is None else retirementThreshold
        self.peakRating = self.setPeakRating() if peakRating is None else peakRating
        self.retired = False
        self.rating = self.getRating()
        self.underlyingSkillDistribution = self.setUnderlyingSkillDistribution() if underlyingSkillDistribution is None else underlyingSkillDistribution
        self.skillDistribution = self.getSkillDistribution()
        self.stats = {skill: self.rating * value for skill, value in self.skillDistribution.items()}
        self.club = None
        self.injured = False
        self.selected = False
    
    def setAge(self):
        agMin = self.config['age']['min']
        agMax = self.config['age']['max']
        return random.randint(agMin, agMax)
    
    def setPeakAge(self):
        return round(Utils.limitedRandNorm(self.config['peakAge']))
    
    def setGrowthSpeed(self):
        randIncline = Utils.limitedRandNorm(self.config['growthSpeed']['incline'])
        randDecline = Utils.limitedRandNorm(self.config['growthSpeed']['decline'])
        return {
            'incline': randIncline,
            'decline': randDecline
        }

    def setRetirementThreshold(self):
        return Utils.limitedRandNorm(self.config['retirementThreshold'])

    def setPeakRating(self):
        return Utils.limitedRandNorm(self.config['peakRating'])

    def getRating(self, age = None):
        age = self.age if age is None else age

        distanceFromPeakAge = abs(self.peakAge - age)
        direction = 'incline' if self.peakAge > age else 'decline'
        growthSpeedFactor = self.growthSpeed[direction]
        peakRatingFulfillment = 1 - (distanceFromPeakAge ** 1.5 * 0.01 * growthSpeedFactor)
        rating = self.peakRating * peakRatingFulfillment
        if direction == 'decline' and rating < (self.peakRating * self.retirementThreshold):
            self.retire()
        return self.peakRating * peakRatingFulfillment

    def rebalanceSkillDistribution(self, distribution):
        [skDiMn, skDiMx] = [value for value in list(self.config['skill']['distribution'].values())[2:4]]
        x = len(self.config['skill']['skills'])
        while True:
            skillsOutOfBounds = []
            for value in distribution.values():
                if value < skDiMn or value > skDiMx:
                    skillsOutOfBounds.append(1)
                else:
                    skillsOutOfBounds.append(0)
            # skillsOutOfBounds = [1 for value in distribution.values() if value < skDiMin or value > skDiMax else 0]
            if not any(skillsOutOfBounds):
                break
            for key, value in distribution.items():
                distribution[key] = ((value * x) + len(distribution) - x) / len(distribution)
            x -= 0.1
    
    def setUnderlyingSkillDistribution(self):
        skills = self.config['skill']['skills']
        [skDiMu, skDiSg] = [value for value in list(self.config['skill']['distribution'].values())[0:2]]
        underlyingSkillDistribution = {skill: np.random.normal(skDiMu, skDiSg) for skill in skills}

        ### Centralise - set mean = 1
        totalSkill = sum(underlyingSkillDistribution.values())
        for key, value in underlyingSkillDistribution.items():
            underlyingSkillDistribution[key] = value * len(skills) / totalSkill
        
        ### Rebalance - handle the passing of thresholds for minimum and maximum
        self.rebalanceSkillDistribution(underlyingSkillDistribution)

        return underlyingSkillDistribution

    def getSkillDistribution(self, age = None):
        skillDistribution = copy.deepcopy(self.underlyingSkillDistribution)

        ### Apply age-dependent modifications to distribution
        age = self.age if age is None else age
        transitions = self.config['skill']['transitions']
        distanceFromPeakAge = self.peakAge - age
        for transition in transitions:
            direction = 'incline' if self.peakAge > age else 'decline'
            if (direction == 'incline' and transition['when']['incline'] == True) or (direction == 'decline' and transition['when']['decline'] == True):
                if transition['from'] == '':
                    toValue = skillDistribution[transition['to']]
                    toFactor = toValue / sum(skillDistribution.values())
                    modifiedToFactor = toFactor - (distanceFromPeakAge * transition['gradient'])
                    skillDistribution[transition['to']] = sum(skillDistribution.values()) * modifiedToFactor
                elif transition['to'] == '':
                    fromValue = skillDistribution[transition['from']]
                    fromFactor = fromValue / sum(skillDistribution.values())
                    modifiedFromFactor = fromFactor - (distanceFromPeakAge * transition['gradient'])
                    skillDistribution[transition['from']] = sum(skillDistribution.values()) * modifiedFromFactor
                else:
                    fromValue = skillDistribution[transition['from']]
                    toValue = skillDistribution[transition['to']]
                    fromToSum = fromValue + toValue
                    fromFactor = fromValue / fromToSum
                    modifiedFromFactor = fromFactor - (distanceFromPeakAge * transition['gradient'])
                    skillDistribution[transition['from']] = fromToSum * modifiedFromFactor
                    skillDistribution[transition['to']] = fromToSum * (1 - modifiedFromFactor)
                self.rebalanceSkillDistribution(skillDistribution)

        ### Set player's best position based on skill distribution
        positions = self.config['positions']
        positionSuitabilities = {}
        selfSkillDistribution = list(skillDistribution.values())
        for position, attributes in positions.items():
            idealSkillDistributionForPosition = list(attributes['skillDistribution'].values())
            positionSuitability = 1 - spatial.distance.cosine(selfSkillDistribution, idealSkillDistributionForPosition)
            if positionSuitability <= 0:
                positionSuitability = 0
            positionSuitabilities[position] = positionSuitability
        self.positionSuitabilities = positionSuitabilities
        self.positionRatings = {key: value * self.rating for key, value in self.positionSuitabilities.items()}
        self.bestPosition = max(positionSuitabilities, key = positionSuitabilities.get)

        ### Now that best position has been identified, normalise player's skill distribution towards the optimum for that position, to curb excessive weirdness
        bestSkillDistribution = self.config['positions'][self.bestPosition]['skillDistribution']
        normalisingFactor = self.config['skill']['normalisingFactor']
        for skill, value in skillDistribution.items():
            skillDistribution[skill] = skillDistribution[skill] + (bestSkillDistribution[skill] - skillDistribution[skill]) * Utils.limitedRandNorm(normalisingFactor)

        return skillDistribution

    def retire(self):
        self.retired = True