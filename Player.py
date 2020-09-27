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
        skills = ['offence', 'spark', 'defence', 'control']
        mu = self.config['skillDistribution']['mean']
        sigma = self.config['skillDistribution']['stDev']
        skillDistribution = {skill: np.random.normal(mu, sigma) for skill in skills}
        totalSkill = sum(skillDistribution.values())
        for key, value in skillDistribution.items():
            skillDistribution[key] = value * 4 / totalSkill

        ### With age, spark decreases and control increases
        distanceFromPeakAge = self.peakAge - self.age
        sparkControlSum = skillDistribution['spark'] + skillDistribution['control']
        sparkFactor = skillDistribution['spark'] / sparkControlSum
        sparkFactor += (distanceFromPeakAge / 100)
        controlFactor = 1 - sparkFactor
        skillDistribution['spark'] = sparkControlSum * sparkFactor
        skillDistribution['control'] = sparkControlSum * controlFactor

        return skillDistribution
    
    def setBestPosition(self):
        positions = self.config['positions']
        positionSuitabilities = {}
        for position, attributes in positions.items():
            # retainedAttributes = {}
            # for attribute in attributes.keys():
            #     if self.skillDistribution[attribute] > attributes[attribute]:
            #         retainedAttributes[attribute] = self.skillDistribution[attribute]
            #         self.skillDistribution[attribute] = attributes[attribute]
            positionSuitability = 1 - spatial.distance.cosine(list(self.skillDistribution.values()), list(attributes.values()))
            if positionSuitability <= 0:
                positionSuitability = 0
            positionSuitabilities[position] = positionSuitability
            # for retainedAttribute, retainedValue in retainedAttributes.items():
            #     self.skillDistribution[retainedAttribute] = retainedValue
        self.positionSuitabilities = positionSuitabilities
        return max(positionSuitabilities, key = positionSuitabilities.get)
        ### Each game a player plays in a particular position, perhaps they get honed more towards it
        ### But also spark should decrease and control increase over time
    
    def retire(self):
        self.retired = True