from config import playerConfig
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
            goals = int(Utils.limitValue(np.random.normal(mu, sigma), 0, 100))
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
    
    def fileMatchReport(self):
        self.competition.handleMatchReport(self.matchReport)