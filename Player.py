import Utilities.Utils as Utils
import random
import numpy as np
from scipy import spatial

class Player:
    def __init__(
        self,
        playerConfig,
        name = None,
        age = None,
        peakAge = None,
        growthSpeed = None,
        retirementThreshold = None,
        peakRating = None,
        skillDistribution = None,
        bestPosition = None
        ):
        self.config = playerConfig
        self.name = Utils.generateName(name, 10) if name == None else name
        self.age = self.setAge() if age == None else age
        self.peakAge = self.setPeakAge() if peakAge == None else peakAge
        self.growthSpeed = self.setGrowthSpeed() if growthSpeed == None else growthSpeed
        self.retirementThreshold = self.setRetirementThreshold() if retirementThreshold == None else retirementThreshold
        self.peakRating = self.setPeakRating() if peakRating == None else peakRating
        self.retired = False
        self.rating = self.calculateRating()
        self.skillDistribution = self.setSkillDistribution() if skillDistribution == None else skillDistribution
        self.bestPosition = self.setBestPosition() if bestPosition == None else bestPosition
        self.team = None
        # randNum = random.randint(1, 1000)
        # if randNum == 1000:
        #     print("Name: {}, Age: {}, PeakRating: {}, Rating: {}".format(self.name, self.age, self.peakRating, self.rating))
    
    def setAge(self):
        minAge = self.config['age']['min']
        maxAge = self.config['age']['max']
        return random.randint(minAge, maxAge)
    
    def setPeakAge(self):
        minPeakAge = self.config['peakAge']['min']
        maxPeakAge = self.config['peakAge']['max']
        return random.randint(minPeakAge, maxPeakAge)
    
    def setGrowthSpeed(self):
        inclineMu = self.config['growthSpeed']['incline']['mean']
        inclineSigma = self.config['growthSpeed']['incline']['stDev']
        declineMu = self.config['growthSpeed']['decline']['mean']
        declineSigma = self.config['growthSpeed']['decline']['stDev']
        return {
            'incline': np.random.normal(inclineMu, inclineSigma),
            'decline': np.random.normal(declineMu, declineSigma)
        }

    def setRetirementThreshold(self):
        mu = self.config['retirementThreshold']['mean']
        sigma = self.config['retirementThreshold']['stDev']
        return np.random.normal(mu, sigma)

    def setPeakRating(self):
        mu = self.config['peakRating']['mean']
        sigma = self.config['peakRating']['stDev']
        return np.random.normal(mu, sigma)

    def calculateRating(self, age = None):
        if age == None:
            age = self.age
        distanceFromPeakAge = abs(self.peakAge - age)
        direction = 'incline' if self.peakAge > age else 'decline'
        growthSpeedFactor = self.growthSpeed[direction]
        peakRatingFulfillment = 1 - (distanceFromPeakAge ** 1.5 * 0.01 * growthSpeedFactor)
        rating = self.peakRating * peakRatingFulfillment
        if direction == 'decline' and rating < (self.peakRating * self.retirementThreshold):
            self.retire()
        return self.peakRating * peakRatingFulfillment
    
    def setSkillDistribution(self):
        skills = self.config['skill']['skills']
        [skDiMu, skDiSigma, skDiMin, skDiMax] = [value for value in self.config['skill']['distribution'].values()]
        skillDistribution = {skill: Utils.limitValue(np.random.normal(skDiMu, skDiSigma), skDiMin, skDiMax) for skill in skills}
        totalSkill = sum(skillDistribution.values())
        for key, value in skillDistribution.items():
            skillDistribution[key] = value * len(skills) / totalSkill

        ### With age, spark decreases and authority increases
        distanceFromPeakAge = self.peakAge - self.age
        sparkAuthoritySum = skillDistribution['spark'] + skillDistribution['authority']
        sparkFactor = skillDistribution['spark'] / sparkAuthoritySum
        sparkFactor += (distanceFromPeakAge / 250)
        skillDistribution['spark'] = sparkAuthoritySum * sparkFactor
        authorityFactor = 1 - sparkFactor
        skillDistribution['authority'] = sparkAuthoritySum * authorityFactor

        ### Fitness drops when player passes peak age
        totalSkill = sum(skillDistribution.values())
        if self.age > self.peakAge:
            fitnessFactor = skillDistribution['fitness'] / totalSkill
            fitnessFactor += (distanceFromPeakAge / 125)
            skillDistribution['fitness'] = Utils.limitValue(totalSkill * fitnessFactor, skDiMin, skDiMax)
        totalSkill = sum(skillDistribution.values())
        for key, value in skillDistribution.items():
            skillDistribution[key] = Utils.limitValue(value * len(skills) / totalSkill, skDiMin, skDiMax)

        return skillDistribution
    
    def setBestPosition(self):
        positions = self.config['positions']
        positionSuitabilities = {}
        selfSkillDistribution = list(self.skillDistribution.values())
        for position, attributes in positions.items():
            idealSkillDistributionForPosition = list(attributes['skillDistribution'].values())
            # retainedAttributes = {}
            # for attribute in attributes.keys():
            #     if self.skillDistribution[attribute] > attributes[attribute]:
            #         retainedAttributes[attribute] = self.skillDistribution[attribute]
            #         self.skillDistribution[attribute] = attributes[attribute]
            positionSuitability = 1 - spatial.distance.cosine(selfSkillDistribution, idealSkillDistributionForPosition)
            if positionSuitability <= 0:
                positionSuitability = 0
            positionSuitabilities[position] = positionSuitability
            # for retainedAttribute, retainedValue in retainedAttributes.items():
            #     self.skillDistribution[retainedAttribute] = retainedValue
        self.positionSuitabilities = positionSuitabilities
        bestPosition = max(positionSuitabilities, key = positionSuitabilities.get)

        ### Now that best position has been identified, normalise player's skill distribution towards the optimum for that position, to curb excessive weirdness
        bestSkillDistribution = self.config['positions'][bestPosition]['skillDistribution']
        normalisingFactor = self.config['skill']['normalisingFactor']
        for skill, value in self.skillDistribution.items():
            self.skillDistribution[skill] = self.skillDistribution[skill] + (bestSkillDistribution[skill] - self.skillDistribution[skill]) * Utils.limitValue(np.random.normal(normalisingFactor['mean'], normalisingFactor['stDev']), normalisingFactor['min'], normalisingFactor['max'])
        
        return bestPosition
        ### Each game a player plays in a particular position, perhaps they get honed more towards it
    
    def retire(self):
        self.retired = True