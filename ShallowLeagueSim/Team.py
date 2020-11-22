from config import playerConfig, matchConfig
import numpy as np
import random

class Team:
    def __init__(self, manager, formation, selection, homeAway):
        self.manager = manager
        self.formation = formation
        self.selection = selection
        self.selectRatings = {}
        self.homeAway = homeAway
        self.setHomeAwayDifferential()
        self.setRating()
        self.normaliseSelectRatings()
        self.setSelectionOffencesDefences()
        self.setTeamOffenceDefence()
        self.setSelectionOffensiveDefensiveContributions()
        self.setGoalAndAssistFactors()
    
    def setHomeAwayDifferential(self):
        if self.homeAway == 'Home':
            self.homeAwayDifferential = 1 + (matchConfig['homeAwayDifferential'] / 2)
        elif self.homeAway == 'Away':
            self.homeAwayDifferential = 1 - (matchConfig['homeAwayDifferential'] / 2)
        else:
            self.homeAwayDifferential = 1
    
    def getSelectFromPlayer(self, player):
        for select in self.selection:
            if select.player == player:
                return select
    
    def getSelectRating(self, select):
        return select.rating
    
    def setRating(self):
        self.rating = np.mean(list(map(self.getSelectRating, self.selection)))
    
    def normaliseSelectRatings(self):
        for select, selectRating in self.selectRatings.items():
            self.selectRatings[select] = ((selectRating * 2) + (self.rating * 1)) / 3

    def getPositionOffenceDefence(self, position):
        positionOffence, positionDefence = 0, 0
        for skill, value in playerConfig['positions'][position]['skillDistribution'].items():
            positionOffence += value * matchConfig['contribution'][skill]['offence']
            positionDefence += value * matchConfig['contribution'][skill]['defence']
        positionOffence /= 3
        positionDefence /= 3
        return {'offence': positionOffence, 'defence': positionDefence}

    def getSelectOffenceDefence(self, select):
        player = select.player
        position = select.position
        positionOffenceDefence = self.getPositionOffenceDefence(position)
        selectRating = self.getSelectRating(select)
        selectOffence, selectDefence = 0, 0
        for skill, value in player.skillDistribution.items():
            selectOffence += (value * selectRating) / 30 * matchConfig['contribution'][skill]['offence'] * positionOffenceDefence['offence']
            selectDefence += (value * selectRating) / 30 * matchConfig['contribution'][skill]['defence'] * positionOffenceDefence['defence']
        return {'offence': selectOffence, 'defence': selectDefence}
    
    def setSelectionOffencesDefences(self):
        self.selectionOffences, self.selectionDefences = {}, {}
        for select in self.selection:
            selectOffenceDefence = self.getSelectOffenceDefence(select)
            self.selectionOffences[select] = selectOffenceDefence['offence']
            self.selectionDefences[select] = selectOffenceDefence['defence']
    
    def setTeamOffenceDefence(self):
        self.offence, self.defence = 0, 0
        for select in self.selection:
            self.offence += self.selectionOffences[select]
            self.defence += self.selectionDefences[select]
    
    def getSelectOffensiveDefensiveContribution(self, select):
        selectOffence, selectDefence = self.selectionOffences[select], self.selectionDefences[select]
        teamOffence, teamDefence = self.offence, self.defence
        return {'offensive': selectOffence / teamOffence, 'defensive': selectDefence / teamDefence}
    
    def setSelectionOffensiveDefensiveContributions(self):
        self.selectionOffensiveContributions, self.selectionDefensiveContributions = {}, {}
        for select in self.selection:
            selectOffensiveDefensiveContribution = self.getSelectOffensiveDefensiveContribution(select)
            self.selectionOffensiveContributions[select] = selectOffensiveDefensiveContribution['offensive']
            self.selectionDefensiveContributions[select] = selectOffensiveDefensiveContribution['defensive']
    
    def getGoals(self, numGoals):
        if numGoals == 0:
            return
        return [self.getGoal() for i in range(numGoals)]
    
    def setGoalAndAssistFactors(self):
        self.setGoalFactors()
        self.setAssistFactors()
    
    def setGoalFactors(self):
        goalFactors = {}
        for select in self.selection:
            position = select.position
            player = select.player
            selectRating = self.getSelectRating(select)
            goalFactor = ((((player.skillDistribution['offence'] * 2) + player.skillDistribution['technique']) / 3) * selectRating * matchConfig['goalLikelihood'][position]) ** 2
            # goalFactor = (player.skillDistribution['offence'] * selectRating * matchConfig['goalLikelihood'][position]) ** 2
            goalFactors[player] = goalFactor
        sumGoalFactors = sum(goalFactors.values())
        self.goalFactors = {player: goalFactor / sumGoalFactors for player, goalFactor in goalFactors.items()}
        
    def setAssistFactors(self):
        assistFactors = {}
        for select in self.selection:
            position = select.position
            player = select.player
            selectRating = self.getSelectRating(select)
            assistFactor = ((((player.skillDistribution['spark'] * 2) + player.skillDistribution['technique']) / 3) * selectRating * matchConfig['assistLikelihood'][position]) ** 1.5 ### The higher this number at the end, the less evenly distributed the assisters will be
            assistFactors[player] = assistFactor
        sumAssistFactors = sum(assistFactors.values())
        self.assistFactors = {player: assistFactor / sumAssistFactors for player, assistFactor in assistFactors.items()}
        
    def getGoal(self):
        goal = {}
        goal['scorer'] = self.getGoalScorer()
        while True:
            assister = self.getGoalAssister()
            if assister != goal['scorer']:
                break
        goal['assister'] = assister
        return goal
    
    def getGoalScorer(self):
        goalscorer = np.random.choice(list(self.goalFactors.keys()), p = list(self.goalFactors.values()))
        return goalscorer
    
    def getGoalAssister(self):
        if np.random.choice([0, 1], p = [0.1, 0.9]) == 0: ### Only 90% of goals are assisted
            return
        assister = np.random.choice(list(self.assistFactors.keys()), p = list(self.assistFactors.values()))
        return assister