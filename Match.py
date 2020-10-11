from config import playerConfig, matchConfig
from goalProbability import goalProbability
import numpy as np
import Utilities.Utils as Utils
import funcy

class Match:
    def __init__(self, competition, clubX, clubY, neutralVenue = False):
        self.competition = competition
        self.clubX, self.clubY = clubX, clubY
        self.clubs = [self.clubX, self.clubY]
        self.matchReport = {club: {} for club in self.clubs}
        report = self.matchReport
        for club in self.clubs:
            report[club]['team'] = club.manager.selectTeam()
        for club in self.clubs: ### Need second round of iteration as the following can only be calculated after both teams have been generated
            oppositionClub = self.clubs[1 - self.clubs.index(club)]
            report[club]['potential'] = report[club]['team'].offence - report[oppositionClub]['team'].defence            
        for club in self.clubs:
            oppositionClub = self.clubs[1 - self.clubs.index(club)]
            report[club]['oppositionClub'] = funcy.omit(report[oppositionClub], 'oppositionClub')

    def play(self):
        report = self.matchReport
        for club in self.clubs:
            report[club]['match'] = {}
            potential = report[club]['potential']
            [mu, sigma] = [value for value in goalProbability[int(potential)].values()]
            goals = int(Utils.limitValue(np.random.normal(mu, sigma), mn = 0, mx = 100))
            report[club]['match']['goalsFor'] = goals
            while True: ### Ensure player's combined goals and assists tally is not higher than the number of goals scored by his team
                report[club]['match']['goalscorers'] = report[club]['team'].getGoalscorers(goals)
                report[club]['match']['assisters'] = report[club]['team'].getAssisters(goals)
                scorersAssisters = report[club]['match']['goalscorers'] + report[club]['match']['assisters']
                if scorersAssisters: ### Prevent max function being applied to an empty list, which throws an error
                    if max([scorersAssisters.count(player) for player in set(scorersAssisters)]) <= goals:
                        break
                else:
                    break
        for club in self.clubs:
            oppositionClub = self.clubs[1 - self.clubs.index(club)]
            report[club]['match']['goalsAgainst'] = report[oppositionClub]['match']['goalsFor']
            if report[club]['match']['goalsFor'] > report[club]['match']['goalsAgainst']:
                report[club]['match']['outcome'] = 'win'
            elif report[club]['match']['goalsFor'] == report[club]['match']['goalsAgainst']:
                report[club]['match']['outcome'] = 'draw'
            else:
                report[club]['match']['outcome'] = 'loss'
        for club in self.clubs:
            team = report[club]['team']
            report[club]['players'] = {}
            playerGoalLikelihoods = self.getPlayerGoalLikelihoods(team)
            playerAssistLikelihoods = self.getPlayerAssistLikelihoods(team)
            for selection in team.teamSelected:
                player = selection['player']
                position = selection['position']
                report[club]['players'][player] = self.getPlayerReport(player, position, playerGoalLikelihoods[player], playerAssistLikelihoods[player])
                ### TODO: Change this so fatigue increase also based on other players' fitness
                player.fatigue += 1 / player.skillDistribution['fitness'] / 5
    
    def getPlayerGoalLikelihoods(self, team):
        goalFactors = {}
        for selection in team.teamSelected:
            position = selection['position']
            player = selection['player']
            positionRating = player.positionRatings[position]
            goalFactor = ((((player.skillDistribution['offence'] * 2) + player.skillDistribution['technique']) / 3) * positionRating * matchConfig['goalLikelihood'][position]) ** 3
            goalFactors[player] = goalFactor
        sumGoalFactors = sum(goalFactors.values())
        goalFactors = {k: v / sumGoalFactors for k, v in goalFactors.items()}
        return goalFactors
    
    def getPlayerAssistLikelihoods(self, team):
        assistFactors = {}
        for selection in team.teamSelected:
            position = selection['position']
            player = selection['player']
            positionRating = player.positionRatings[position]
            assistFactor = ((((player.skillDistribution['spark'] * 2) + player.skillDistribution['technique']) / 3) * positionRating * matchConfig['assistLikelihood'][position]) ** 2
            assistFactors[player] = assistFactor
        sumAssistFactors = sum(assistFactors.values())
        assistFactors = {k: v / sumAssistFactors for k, v in assistFactors.items()}
        return assistFactors

    def getPlayerReport(self, player, position, playerGoalLikelihood, playerAssistLikelihood):
        playerReport = {}
        playerReport['position'] = position
        playerReport['fatigue'] = player.fatigue
        club = player.club
        oppositionClub = self.clubs[1 - self.clubs.index(club)]
        clubReport = self.matchReport[club]
        oppositionClubReport = self.matchReport[oppositionClub]
        for i, j in zip(['goalscorers', 'assisters'], ['goals', 'assists']):
            x = clubReport['match'][i]
            playerReport[j] = x.count(player)

        ### Get player performance index
        baseRating = np.random.normal((player.rating / 10) - 1, 0.5)
        positionSuitability = player.positionSuitabilities[position]
        playerOffence, playerDefence = 0, 0
        for key, value in player.stats.items():
            value *= positionSuitability
            playerOffence += value * matchConfig['contribution'][key]['offence']
            playerDefence += value * matchConfig['contribution'][key]['defence']
        playerOffence, playerDefence = playerOffence / 30, playerDefence / 30
        teamOffence = clubReport['team'].offence
        teamDefence = clubReport['team'].defence
        offensiveContribution = playerOffence / teamOffence
        defensiveContribution = playerDefence / teamDefence
        teamPredictedGoalsFor = goalProbability[int(clubReport['potential'])]['mu']
        teamActualGoalsFor = clubReport['match']['goalsFor']
        teamOffensiveOutperformance = teamActualGoalsFor - teamPredictedGoalsFor
        teamPredictedGoalsAgainst = goalProbability[int(oppositionClubReport['potential'])]['mu']
        teamActualGoalsAgainst = oppositionClubReport['match']['goalsFor']
        teamDefensiveOutperformance = teamPredictedGoalsAgainst - teamActualGoalsAgainst
        offensiveBoost = offensiveContribution * teamOffensiveOutperformance * 5
        defensiveBoost = defensiveContribution * teamDefensiveOutperformance * 5
        playerPredictedGoals = teamPredictedGoalsFor * playerGoalLikelihood
        ratingBoostForGoal = 1
        goalNegative = playerPredictedGoals * ratingBoostForGoal
        goalPositive = playerReport['goals'] * ratingBoostForGoal
        playerPredictedAssists = teamPredictedGoalsFor * 0.9 * playerAssistLikelihood
        ratingBoostForAssist = 0.75
        assistNegative = playerPredictedAssists * ratingBoostForAssist
        assistPositive = playerReport['assists'] * ratingBoostForAssist
        performanceIndex = Utils.limitValue(
            baseRating + offensiveBoost + defensiveBoost - goalNegative + goalPositive - assistNegative + assistPositive,
            mn = 0,
            mx = 10
        )
        playerReport['performanceIndex'] = performanceIndex

        return playerReport
    
    def fileMatchReport(self):
        self.competition.handleMatchReport(self.matchReport)