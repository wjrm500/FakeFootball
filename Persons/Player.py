import sys
sys.path.append('.')
from Persons.Person import Person
import Utilities.Utils as Utils
import random
import numpy as np
from scipy import spatial
from config import playerConfig
import copy
from datetime import date, timedelta

class Player(Person):
    def __init__(
        self,
        personController,
        id,
        name = None,
        age = None,
        config = None,
        peakAge = None,
        growthSpeed = None,
        retirementThreshold = None,
        peakRating = None,
        underlyingSkillDistribution = None
        ):
        super(Player, self).__init__(personController, id, name, age)
        self.config = copy.deepcopy(playerConfig)
        if config is not None and config != playerConfig:
            Utils.updateConfig(self.config, config)
        self.setPeakAge(peakAge)
        self.setGrowthSpeed(growthSpeed)
        self.setRetirementThreshold(retirementThreshold)
        self.setPeakRating(peakRating)
        self.retired = False
        self.setRating()
        self.setUnderlyingSkillDistribution(underlyingSkillDistribution)
        self.setSkillDistribution()
        self.setSkillValues()
        self.club = None
        self.injured = False
        self.fatigue = 0
        self.playerReports = []
        self.injuries = []
        self.form = 0
        self.ratings = {}
        self.forms = {}
    
    def setPeakAge(self, peakAge):
        self.peakAge = peakAge if peakAge is not None else Utils.limitedRandNorm(self.config['peakAge'])
    
    def setGrowthSpeed(self, growthSpeed):
        if growthSpeed is not None:
            self.growthSpeed = growthSpeed
        else:
            randIncline = Utils.limitedRandNorm(self.config['growthSpeed']['incline'])
            randDecline = Utils.limitedRandNorm(self.config['growthSpeed']['decline'])
            self.growthSpeed = {
                'incline': randIncline,
                'decline': randDecline
            }

    def setRetirementThreshold(self, retirementThreshold):
        self.retirementThreshold = retirementThreshold if retirementThreshold is not None else Utils.limitedRandNorm(self.config['retirementThreshold'])

    def setPeakRating(self, peakRating):
        self.peakRating = peakRating if peakRating is not None else Utils.limitedRandNorm(self.config['peakRating'])

    def adjustPeakRating(self):
        mn, mx = self.config['peakRating']['min'], self.config['peakRating']['max']
        self.peakRating = Utils.limitedRandNorm({'mu': self.peakRating, 'sigma': 50 / (self.age ** 2), 'mn': mn, 'mx': mx})

    def setRating(self, age = None):
        age = age if age is not None else self.age
        distanceFromPeakAge = abs(self.peakAge - age)
        direction = 'incline' if self.peakAge > age else 'decline'
        growthSpeedFactor = self.growthSpeed[direction]
        peakRatingFulfillment = 1 - (distanceFromPeakAge ** 1.5 * 0.01 * growthSpeedFactor)
        rating = self.peakRating * peakRatingFulfillment
        if direction == 'decline' and rating < (self.peakRating * self.retirementThreshold) and self.retired is False:
            self.retire()
        self.rating = self.peakRating * peakRatingFulfillment

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
    
    def setUnderlyingSkillDistribution(self, underlyingSkillDistribution):
        skills = self.config['skill']['skills']
        [skDiMu, skDiSg] = [value for value in list(self.config['skill']['distribution'].values())[0:2]]
        underlyingSkillDistribution = {skill: np.random.normal(skDiMu, skDiSg) for skill in skills}

        ### Centralise - set mean = 1
        totalSkill = sum(underlyingSkillDistribution.values())
        for key, value in underlyingSkillDistribution.items():
            underlyingSkillDistribution[key] = value * len(skills) / totalSkill
        
        ### Rebalance - handle the passing of thresholds for minimum and maximum
        self.rebalanceSkillDistribution(underlyingSkillDistribution)

        self.underlyingSkillDistribution = underlyingSkillDistribution

    def setSkillDistribution(self, age = None):
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

        self.skillDistribution = skillDistribution
    
    def setSkillValues(self):
        self.skillValues = {skill: self.rating * value for skill, value in self.skillDistribution.items()}

    def retire(self):
        self.retired = True
        if self in self.personController.activePlayers:
            self.personController.activePlayers.remove(self)
        self.personController.retiredPlayers.append(self)
        if hasattr(self, 'club') and self.club:
            self.club.squad.remove(self)
            self.club = None
    
    def recover(self):
        fatigueReduction = np.sqrt(self.skillValues['fitness']) / 50
        self.fatigue -= fatigueReduction
        self.fatigue = 0 if self.fatigue < 0 else self.fatigue
        if self.injured:
            self.injured -= 1
        if self.injured == 0:
            self.injured = False
        self.form -= self.form / 25
    
    def injure(self):
        if self.injured is False:
            injury = True if np.random.normal(self.fatigue, 0.02) > 0.25 else False
            if injury:
                x, itemArray, probabilityArray = 1, [], []
                for i in range(1, 366):
                    x /= 1.05
                    itemArray.append(i)
                    probabilityArray.append(x)
                probabilityArray = [probability / sum(probabilityArray) for probability in probabilityArray]
                injuryLength = np.random.choice(itemArray, p = probabilityArray)
                self.injured = injuryLength
                self.injuries.append([self.personController.universe.timeLord.currentDate, injuryLength])

    def advance(self):
        self.injure()
        super().advance()
        self.recover()
        self.adjustPeakRating()
        self.setRating()
        self.setSkillDistribution()
        self.setSkillValues()
        self.storeRatingsAndForm()
    
    def handlePlayerReport(self, playerReport):
        if playerReport not in self.playerReports: ### Prevent duplication from Universal Tournament group stage matches, which are handled by both the group and the wider tournament
            self.playerReports.append(playerReport)
            outperformance = playerReport['performanceIndex'] - playerReport['performanceData']['baseRating']
            gameFormValue = outperformance / 2
            gravity = self.form / 2
            self.form += (gameFormValue - gravity)
            self.form = Utils.limitValue(self.form, mn = -10, mx = 10)
    
    def displayPlayerReports(self):
        for playerReport in self.playerReports:
            print(
                '{:10} --- {:30} --- Position: {} --- Goals: {} --- Assists: {} --- Performance Index: {:.2f}'.format(
                    playerReport['date'].strftime('%d/%m/%Y'),
                    type(playerReport['tournament']).__name__,
                    playerReport['position'],
                    playerReport['goals'],
                    playerReport['assists'],
                    playerReport['performanceIndex']
                )
            )
    
    def getPerformanceIndices(self):
        if len(self.playerReports) == 0:
            return None
        seasonData = {}
        for playerReport in self.playerReports:
            if not seasonData.get(playerReport['tournament']):
                seasonData[playerReport['tournament']] = {
                    'games': 0,
                    'goals': 0,
                    'assists': 0,
                    'performanceIndex': []
                }
            seasonData[playerReport['tournament']]['games'] += 1
            seasonData[playerReport['tournament']]['goals'] += playerReport['goals']
            seasonData[playerReport['tournament']]['assists'] += playerReport['assists']
            seasonData[playerReport['tournament']]['performanceIndex'].append(playerReport['performanceIndex'])
        for tournament, data in seasonData.items():
            seasonData[tournament]['performanceIndex'] = np.mean(data['performanceIndex'])
        overallSeasonData = {}
        for metric in ['games', 'goals', 'assists']:
            overallSeasonData[metric] = sum([data[metric] for data in seasonData.values()])
        overallSeasonData['performanceIndex'] = sum([data['games'] * data['performanceIndex'] for data in seasonData.values()]) / sum([data['games'] for data in seasonData.values()])
        return [seasonData, overallSeasonData]

    def displayPerformanceIndices(self):
        if len(self.playerReports) == 0:
            return None
        seasonData, overallSeasonData = self.getPerformanceIndices()
        print('{:20}{:>46}'.format(
            self.properName,
            '{} rated {:3}'.format(int(self.rating), self.bestPosition)
            )
        )
        print('-' * 66)
        for tournament, data in seasonData.items():
            print('{:30} - GP: {:2} - G: {:2} - A: {:2} - PI: {:.2f}'.format(
                type(tournament).__name__,
                data['games'],
                data['goals'],
                data['assists'],
                data['performanceIndex']
                )
            )
        print('-' * 66)
        print('{:30} - GP: {:2} - G: {:2} - A: {:2} - PI: {:.2f}'.format(
                'Total',
                overallSeasonData['games'],
                overallSeasonData['goals'],
                overallSeasonData['assists'],
                overallSeasonData['performanceIndex']
                )
            )
    
    def displayOneLinePerformanceIndices(self, competitions):
        if len(self.playerReports) == 0:
            return None
        seasonData, overallSeasonData = self.getPerformanceIndices()
        printArray = []
        for competition in competitions:
            if seasonData.get(competition):
                data = seasonData[competition]
                printArray.append('{:2} / {:2} / {:2} / {}'.format(data['games'], data['goals'], data['assists'], str(data['performanceIndex'])[:4]))
            else:
                printArray.append('{:2} / {:2} / {:2} / {:.2f}'.format(0, 0, 0, 0))
        printArray.append('{:2} / {:2} / {:2} / {}'.format(
            overallSeasonData['games'],
            overallSeasonData['goals'],
            overallSeasonData['assists'],
            str(overallSeasonData['performanceIndex'])[:4]
            )
        )
        joiner = ' ' * 5
        printArray = joiner.join(printArray)
        print('{:25} {:15} {}'.format(self.properName, '{} rated {:3}'.format(int(self.rating), self.bestPosition), printArray))
                

    def storeRatingsAndForm(self):
        currentDate = self.personController.universe.timeLord.currentDate
        self.ratings[currentDate] = self.rating
        self.forms[currentDate] = self.form