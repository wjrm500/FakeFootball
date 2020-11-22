from Person import Person
import Utils
import numpy as np
from scipy import spatial
from config import playerConfig
import copy
from scipy import spatial

class Player(Person):
    def __init__(self):
        super().__init__()
        self.setPeakAge()
        self.setPeakRating()
        self.setRating()
        self.setUnderlyingSkillDistribution()
        self.setSkillDistribution()
        self.setSkillValues()
        self.injured = False
        self.fatigue = 0
        self.form = 0
        self.club = None
    
    def setPeakAge(self):
        self.peakAge = Utils.limitedRandNorm(playerConfig['peakAge'])
    
    def setPeakRating(self):
        self.peakRating = Utils.limitedRandNorm(playerConfig['peakRating'])

    def setRating(self):
        distanceFromPeakAge = abs(self.peakAge - self.age)
        peakRatingFulfillment = 1 - (distanceFromPeakAge ** 1.5 * 0.01 * 0.75)
        self.rating = self.peakRating * peakRatingFulfillment
        if self.age > self.peakAge and self.rating < (self.peakRating * playerConfig['retirementThreshold']['mean']) and self.retired is False:
            self.retire()

    def setUnderlyingSkillDistribution(self):
        skills = playerConfig['skill']['skills']
        [skDiMu, skDiSg] = [value for value in list(playerConfig['skill']['distribution'].values())[0:2]]
        underlyingSkillDistribution = {skill: np.random.normal(skDiMu, skDiSg) for skill in skills}

        ### Centralise - set mean = 1
        totalSkill = sum(underlyingSkillDistribution.values())
        for key, value in underlyingSkillDistribution.items():
            underlyingSkillDistribution[key] = value * len(skills) / totalSkill
        
        ### Rebalance - handle the passing of thresholds for minimum and maximum
        self.rebalanceSkillDistribution(underlyingSkillDistribution)

        self.underlyingSkillDistribution = underlyingSkillDistribution

    def rebalanceSkillDistribution(self, distribution):
        [skDiMn, skDiMx] = [value for value in list(playerConfig['skill']['distribution'].values())[2:4]]
        x = len(playerConfig['skill']['skills'])
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

    def setSkillDistribution(self):
        skillDistribution = copy.deepcopy(self.underlyingSkillDistribution)

        ### Apply age-dependent modifications to distribution
        transitions = playerConfig['skill']['transitions']
        distanceFromPeakAge = self.peakAge - self.age
        for transition in transitions:
            direction = 'incline' if self.peakAge > self.age else 'decline'
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
        positions = playerConfig['positions']
        positionSuitabilities = {}
        selfSkillDistribution = list(skillDistribution.values())
        for position, attributes in positions.items():
            idealSkillDistributionForPosition = list(attributes['skillDistribution'].values())
            positionSuitability = 1 - spatial.distance.cosine(selfSkillDistribution, idealSkillDistributionForPosition)
            positionSuitability = 1 - np.power(1 - positionSuitability, (2 / 3))
            if positionSuitability <= 0:
                positionSuitability = 0
            positionSuitabilities[position] = positionSuitability
        maxPositionSuitability = max(positionSuitabilities.values())	
        for position in positionSuitabilities.keys():	
            positionSuitabilities[position] *= 1 / maxPositionSuitability
        self.positionSuitabilities = positionSuitabilities
        self.positionRatings = {key: value * self.rating for key, value in self.positionSuitabilities.items()}
        self.bestPosition = max(positionSuitabilities, key = positionSuitabilities.get)

        ### Now that best position has been identified, normalise player's skill distribution towards the optimum for that position, to curb excessive weirdness
        bestSkillDistribution = playerConfig['positions'][self.bestPosition]['skillDistribution']
        normalisingFactor = playerConfig['skill']['normalisingFactor']
        for skill, value in skillDistribution.items():
            skillDistribution[skill] = skillDistribution[skill] + (bestSkillDistribution[skill] - skillDistribution[skill]) * Utils.limitedRandNorm(normalisingFactor)

        ### Centralise - restore mean to 1
        totalSkill = sum(skillDistribution.values())
        for key, value in skillDistribution.items():
            skillDistribution[key] = value * len(skillDistribution.values()) / totalSkill

        self.skillDistribution = skillDistribution
    
    def setSkillValues(self):
        self.skillValues = {skill: self.rating * value for skill, value in self.skillDistribution.items()}

    def handlePlayerReport(self, playerReport):
        self.fatigue += playerReport['fatigueIncrease']
        self.form += playerReport['gravitatedMatchForm']
        self.recover()
        self.injure()
    
    def recover(self):
        fatigueReduction = np.sqrt(self.skillValues['fitness']) / 100 * 4
        self.fatigue -= fatigueReduction
        self.fatigue = 0 if self.fatigue < 0 else self.fatigue
        if self.injured:
            self.injured -= 1
        if self.injured == 0:
            self.injured = False
        self.form -= self.form / 25
    
    def injure(self):
        if self.injured is False:
            injury = True if np.random.normal(self.fatigue, 0.05) > 0.5 else False
            if injury:
                x, itemArray, probabilityArray = 1, [], []
                for i in range(1, 366):
                    x /= 1.05
                    itemArray.append(i)
                    probabilityArray.append(x)
                probabilityArray = [probability / sum(probabilityArray) for probability in probabilityArray]
                injuryLength = np.random.choice(itemArray, p = probabilityArray)
                self.injured = injuryLength

    # def getDiversity(self):
    #     euclideanDistances = []
    #     otherPlayersAtClub = [player for player in self.club.squad if player is not self]
    #     for otherPlayer in otherPlayersAtClub:
    #         euclideanDistances.append(
    #             spatial.distance.euclidean(
    #                 list(self.skillDistribution.values()),
    #                 list(otherPlayer.skillDistribution.values())
    #             )
    #         )
    #     return np.mean(euclideanDistances)
    
    def getFutureVersion(self, yearsIntoFuture):
        futureVersion = copy.deepcopy(self)
        futureVersion.age += yearsIntoFuture
        futureVersion.setRating()
        futureVersion.setSkillDistribution()
        futureVersion.setSkillValues()
        return futureVersion

    def retire(self):
        self.retired = True
        if hasattr(self, 'club') and self.club:
            self.club.squad.remove(self)
            self.club = None
    
    def inTopThreePositions(self, position):
        topThreePositions = list(map(lambda x: x[0], sorted(self.positionRatings.items(), key = lambda x: x[1])))[-3:]
        return position in topThreePositions