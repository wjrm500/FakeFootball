from config import playerConfig, matchConfig
from goalProbability import goalProbability
import numpy as np
import Utilities.Utils as Utils
import funcy

class Match:
    def __init__(self, fixture, tournament, date, clubX, clubY, neutralVenue = False):
        ### TODO: Home advantage
        self.fixture = fixture
        self.tournament = tournament
        self.date = date
        self.clubX, self.clubY = clubX, clubY
        self.clubs = [self.clubX, self.clubY]
        self.matchReport = {'tournament': self.tournament, 'date': self.date, 'clubs': {club: {} for club in self.clubs}}
        report = self.matchReport
        for club in self.clubs:
            report['clubs'][club]['team'] = club.manager.selectTeam()
        for club in self.clubs: ### Need second round of iteration as the following can only be calculated after both teams have been generated
            oppositionClub = self.getOppositionClub(club)
            report['clubs'][club]['potential'] = report['clubs'][club]['team'].offence - report['clubs'][oppositionClub]['team'].defence            
        for club in self.clubs:
            oppositionClub = self.getOppositionClub(club)
            report['clubs'][club]['oppositionClub'] = funcy.omit(report['clubs'][oppositionClub], 'oppositionClub')

    def getOppositionClub(self, club):
        return self.clubs[1 - self.clubs.index(club)]

    def play(self):
        report = self.matchReport
        for club in self.clubs:
            if report['clubs'][club]['team'] == None:
                continue
            report['clubs'][club]['match'] = {}
            potential = report['clubs'][club]['potential']
            [mu, sigma] = [value for value in goalProbability[int(potential)].values()]
            goals = int(Utils.limitValue(np.random.normal(mu, sigma), mn = 0, mx = 100))
            report['clubs'][club]['match']['goalsFor'] = goals
            while True: ### Ensure player's combined goals and assists tally is not higher than the number of goals scored by his team
                report['clubs'][club]['match']['goalscorers'] = report['clubs'][club]['team'].getGoalscorers(goals)
                report['clubs'][club]['match']['assisters'] = report['clubs'][club]['team'].getAssisters(goals)
                scorersAssisters = report['clubs'][club]['match']['goalscorers'] + report['clubs'][club]['match']['assisters']
                if scorersAssisters: ### Prevent max function being applied to an empty list, which throws an error
                    if max([scorersAssisters.count(player) for player in set(scorersAssisters)]) <= goals:
                        break
                else:
                    break
        for club in self.clubs:
            oppositionClub = self.getOppositionClub(club)
            report['clubs'][club]['match']['goalsAgainst'] = report['clubs'][oppositionClub]['match']['goalsFor']
            if report['clubs'][club]['match']['goalsFor'] > report['clubs'][club]['match']['goalsAgainst']:
                report['clubs'][club]['match']['outcome'] = 'win'
                self.matchReport['winner'] = club
            elif report['clubs'][club]['match']['goalsFor'] == report['clubs'][club]['match']['goalsAgainst']:
                report['clubs'][club]['match']['outcome'] = 'draw'
            else:
                report['clubs'][club]['match']['outcome'] = 'loss'
        meanFitness = np.mean([select.player.skillValues['fitness'] for club in self.clubs for select in report['clubs'][club]['team'].selection])
        for club in self.clubs:
            team = report['clubs'][club]['team']
            report['clubs'][club]['players'] = {}
            playerGoalLikelihoods = self.getPlayerGoalLikelihoods(team)
            playerAssistLikelihoods = self.getPlayerAssistLikelihoods(team)
            for select in team.selection:
                player = select.player
                position = select.position
                report['clubs'][club]['players'][player] = self.getPlayerReport(player, position, playerGoalLikelihoods[player], playerAssistLikelihoods[player])
                fitnessFromMean = meanFitness - player.skillValues['fitness']
                mu = (np.power(np.e, fitnessFromMean / 10) / (np.power(np.e, fitnessFromMean / 10) + 1)) / 5
                player.fatigue += Utils.limitedRandNorm({'mu': mu, 'sg': 0.02, 'mn': 0, 'mx': 0.25})
    
    def getPlayerGoalLikelihoods(self, team):
        goalFactors = {}
        for select in team.selection:
            player = select.player
            position = select.position
            positionRating = player.positionRatings[position]
            goalFactor = ((((player.skillDistribution['offence'] * 2) + player.skillDistribution['technique']) / 3) * positionRating * matchConfig['goalLikelihood'][position]) ** 3
            goalFactors[player] = goalFactor
        sumGoalFactors = sum(goalFactors.values())
        goalFactors = {k: v / sumGoalFactors for k, v in goalFactors.items()}
        return goalFactors
    
    def getPlayerAssistLikelihoods(self, team):
        assistFactors = {}
        for select in team.selection:
            position = select.position
            player = select.player
            positionRating = player.positionRatings[position]
            assistFactor = ((((player.skillDistribution['spark'] * 2) + player.skillDistribution['technique']) / 3) * positionRating * matchConfig['assistLikelihood'][position]) ** 2
            assistFactors[player] = assistFactor
        sumAssistFactors = sum(assistFactors.values())
        assistFactors = {k: v / sumAssistFactors for k, v in assistFactors.items()}
        return assistFactors

    def getPlayerReport(self, player, position, playerGoalLikelihood, playerAssistLikelihood):
        playerReport = {}
        playerReport['tournament'] = self.tournament 
        playerReport['date'] = self.date
        playerReport['position'] = position
        playerReport['fatigue'] = player.fatigue
        playerReport['performanceData'] = {} ### TAGGED AS TEMPORARY
        club = player.club
        oppositionClub = self.getOppositionClub(club)
        clubReport = self.matchReport['clubs'][club]
        oppositionClubReport = self.matchReport['clubs'][oppositionClub]
        for i, j in zip(['goalscorers', 'assisters'], ['goals', 'assists']):
            x = clubReport['match'][i]
            playerReport[j] = x.count(player)

        ### Get player performance index
        playerReport['performanceData']['playerRating'] = player.rating ### TAGGED AS TEMPORARY
        playerReport['performanceData']['oppositionTeamRating'] = oppositionClubReport['team'].rating ### TAGGED AS TEMPORARY
        if player.rating - oppositionClubReport['team'].rating < 0:
            baseRating = 5 - (np.power(abs((player.rating - oppositionClubReport['team'].rating) / 5), (2 / 3)))
        else:
            baseRating = 5 + (np.power((player.rating - oppositionClubReport['team'].rating) / 5, (2 / 3)))
        baseRating = Utils.limitedRandNorm({'mu': baseRating, 'sg': 0.5, 'mn': 1, 'mx': 9})
        select = clubReport['team'].getSelectFromPlayer(player)
        offensiveContribution = clubReport['team'].selectionOffensiveContributions[select]
        defensiveContribution = clubReport['team'].selectionDefensiveContributions[select]
        teamPredictedGoalsFor = Utils.limitValue(goalProbability[int(clubReport['potential'])]['mu'], mn = 0)
        teamActualGoalsFor = clubReport['match']['goalsFor']
        teamOffensiveOutperformance = teamActualGoalsFor - teamPredictedGoalsFor
        teamPredictedGoalsAgainst = Utils.limitValue(goalProbability[int(oppositionClubReport['potential'])]['mu'], mn = 0)
        teamActualGoalsAgainst = oppositionClubReport['match']['goalsFor']
        teamDefensiveOutperformance = teamPredictedGoalsAgainst - teamActualGoalsAgainst
        offensiveBoost = Utils.limitValue(offensiveContribution * teamOffensiveOutperformance * 5, mx = 1.5)
        defensiveBoost = Utils.limitValue(defensiveContribution * teamDefensiveOutperformance * 5, mx = 1.5)
        playerReport['performanceData']['baseRating'] = baseRating ### TAGGED AS TEMPORARY
        playerReport['performanceData']['offensiveContribution'] = offensiveContribution ### TAGGED AS TEMPORARY
        playerReport['performanceData']['defensiveContribution'] = defensiveContribution ### TAGGED AS TEMPORARY
        playerReport['performanceData']['teamPredictedGoalsFor'] = teamPredictedGoalsFor ### TAGGED AS TEMPORARY
        playerReport['performanceData']['teamActualGoalsFor'] = teamActualGoalsFor ### TAGGED AS TEMPORARY
        playerReport['performanceData']['teamOffensiveOutperformance'] = teamOffensiveOutperformance ### TAGGED AS TEMPORARY
        playerReport['performanceData']['teamPredictedGoalsAgainst'] = teamPredictedGoalsAgainst ### TAGGED AS TEMPORARY
        playerReport['performanceData']['teamActualGoalsAgainst'] = teamActualGoalsAgainst ### TAGGED AS TEMPORARY
        playerReport['performanceData']['teamDefensiveOutperformance'] = teamDefensiveOutperformance ### TAGGED AS TEMPORARY
        playerReport['performanceData']['offensiveBoost'] = offensiveBoost ### TAGGED AS TEMPORARY
        playerReport['performanceData']['defensiveBoost'] = defensiveBoost ### TAGGED AS TEMPORARY
        playerPredictedGoals = teamPredictedGoalsFor * playerGoalLikelihood
        ratingBoostForGoal = 1.5
        goalNegative = playerPredictedGoals * ratingBoostForGoal / 2 ### Dividing by 2 is a new addition intended to boost goal involvements and help compensate for the disproportionate effects of any potential 10-cap
        goalPositive = playerReport['goals'] * ratingBoostForGoal
        playerPredictedAssists = teamPredictedGoalsFor * 0.9 * playerAssistLikelihood
        ratingBoostForAssist = 1
        assistNegative = playerPredictedAssists * ratingBoostForAssist  / 2 ### Dividing by 2 is a new addition
        assistPositive = playerReport['assists'] * ratingBoostForAssist
        playerReport['performanceData']['predictedGoals'] = playerPredictedGoals ### TAGGED AS TEMPORARY
        playerReport['performanceData']['goalNegative'] = goalNegative ### TAGGED AS TEMPORARY
        playerReport['performanceData']['goalPositive'] = goalPositive ### TAGGED AS TEMPORARY
        playerReport['performanceData']['predictedAssists'] = playerPredictedAssists ### TAGGED AS TEMPORARY
        playerReport['performanceData']['assistNegative'] = assistNegative ### TAGGED AS TEMPORARY
        playerReport['performanceData']['assistPositive'] = assistPositive ### TAGGED AS TEMPORARY
        performanceIndex = Utils.limitValue(
            baseRating + offensiveBoost + defensiveBoost - goalNegative + goalPositive - assistNegative + assistPositive,
            mn = 0,
            mx = 10
        )
        playerReport['performanceIndex'] = performanceIndex
        return playerReport
    
    def fileMatchReport(self):
        self.fixture.handleMatchReport(self.matchReport)
        self.tournament.handleMatchReport(self.matchReport)