from config import playerConfig, matchConfig
from numpy.random import choice

class Team:
    def __init__(self, manager, formation, teamSelected):
        self.manager = manager
        self.club = self.manager.club
        self.formation = formation
        self.teamSelected = teamSelected
        self.setAttributes()
        self.setOffenceDefence()
        
    def setAttributes(self):
        attributes = {skill: 0 for skill in playerConfig['skill']['skills']}
        for selection in self.teamSelected:
            position = selection['position']
            player = selection['player']
            positionRating = player.positionRatings[position]
            for skill, value in player.skillDistribution.items():
                attributes[skill] += (value * positionRating) / 10
        self.attributes = attributes
    
    def setOffenceDefence(self):
        self.offence, self.defence = 0, 0
        for attributeKey in self.attributes.keys():
            self.offence += self.attributes[attributeKey] * matchConfig['contribution'][attributeKey]['offence']
            self.defence += self.attributes[attributeKey] * matchConfig['contribution'][attributeKey]['defence']
        self.offence, self.defence = self.offence / 3, self.defence / 3
    
    def getGoalscorers(self, numGoals):
        goalFactors = {}
        for selection in self.teamSelected:
            position = selection['position']
            player = selection['player']
            positionRating = player.positionRatings[position]
            goalFactor = ((((player.skillDistribution['offence'] * 2) + player.skillDistribution['technique']) / 3) * positionRating * matchConfig['goalLikelihood'][position]) ** 3
            goalFactors[player] = goalFactor
        sumGoalFactors = sum(goalFactors.values())
        goalFactors = {player: goalFactor / sumGoalFactors for player, goalFactor in goalFactors.items()}
        goalscorers = list(choice(list(goalFactors.keys()), size = numGoals, p = list(goalFactors.values())))
        return goalscorers
    
    def getAssisters(self, numAssists):
        numAssists = sum([choice([0, 1], p = [0.1, 0.9]) for i in range(numAssists)]) ### Only 90% of goals are assisted
        assistFactors = {}
        for selection in self.teamSelected:
            position = selection['position']
            player = selection['player']
            positionRating = player.positionRatings[position]
            assistFactor = ((((player.skillDistribution['spark'] * 2) + player.skillDistribution['technique']) / 3) * positionRating * matchConfig['assistLikelihood'][position]) ** 2
            assistFactors[player] = assistFactor
        sumAssistFactors = sum(assistFactors.values())
        assistFactors = {player: assistFactor / sumAssistFactors for player, assistFactor in assistFactors.items()}
        assisters = list(choice(list(assistFactors.keys()), size = numAssists, p = list(assistFactors.values())))
        return assisters