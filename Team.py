from config import playerConfig, matchConfig
import numpy as np

class Team:
    ### Definitions
    ### Noun 'Select' - An entity comprising a player and a position, binded as a tuple
    ### Noun 'Selection' - An array or collection of Selects
    ### Noun 'Team' - A superlative entity whose values arise from the aggregation of values in a Selection
    def __init__(self, manager, formation, selection):
        self.manager = manager
        self.club = self.manager.club
        self.formation = formation
        self.selection = selection
        self.players = [select.player for select in selection]
        self.setRating()
        self.setSelectionOffencesDefences()
        self.setTeamOffenceDefence()
        self.setSelectionOffensiveDefensiveContributions()
    
    def getSelectFromPlayer(self, player):
        for select in self.selection:
            if select.player == player:
                return select
    
    def getSelectRating(self, select):
        player = select.player
        position = select.position
        selectRating = player.positionRatings[position]
        return selectRating - (selectRating * player.fatigue)
    
    def setRating(self):
        self.rating = np.mean(list(map(self.getSelectRating, self.selection)))

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
    
    def getGoalscorers(self, numGoals):
        goalFactors = {}
        for select in self.selection:
            position = select.position
            player = select.player
            positionRating = player.positionRatings[position]
            goalFactor = ((((player.skillDistribution['offence'] * 2) + player.skillDistribution['technique']) / 3) * positionRating * matchConfig['goalLikelihood'][position]) ** 3
            goalFactors[player] = goalFactor
        sumGoalFactors = sum(goalFactors.values())
        goalFactors = {player: goalFactor / sumGoalFactors for player, goalFactor in goalFactors.items()}
        goalscorers = list(np.random.choice(list(goalFactors.keys()), size = numGoals, p = list(goalFactors.values())))
        return goalscorers
    
    def getAssisters(self, numAssists):
        numAssists = sum([np.random.choice([0, 1], p = [0.1, 0.9]) for i in range(numAssists)]) ### Only 90% of goals are assisted
        assistFactors = {}
        for select in self.selection:
            position = select.position
            player = select.player
            positionRating = player.positionRatings[position]
            assistFactor = ((((player.skillDistribution['spark'] * 2) + player.skillDistribution['technique']) / 3) * positionRating * matchConfig['assistLikelihood'][position]) ** 2
            assistFactors[player] = assistFactor
        sumAssistFactors = sum(assistFactors.values())
        assistFactors = {player: assistFactor / sumAssistFactors for player, assistFactor in assistFactors.items()}
        assisters = list(np.random.choice(list(assistFactors.keys()), size = numAssists, p = list(assistFactors.values())))
        return assisters