from Match import Match

class Fixture:
    def __init__(self, tournament, date = None, clubX = None, clubY = None):
        self.tournament = tournament
        self.date = date
        self.addClubs(clubX, clubY)
        self.played = False
    
    def addClubs(self, clubX, clubY):
        self.clubX, self.clubY = clubX, clubY
        self.clubs = [self.clubX, self.clubY]
    
    def setDate(self, date):
        self.date = date
    
    def setGameweek(self, gameweek):
        self.gameweek = gameweek

    def play(self):
        self.match = Match(self, self.tournament, self.date, self.clubX, self.clubY)
        self.match.play()
        self.match.fileMatchReport()
        self.played = True
        if type(self.tournament).__name__ != 'League':
            if type(self.tournament).__name__ == 'Group':
                self.tournament.tournament.checkAdvance()
            else:
                self.tournament.checkAdvance()
    
    def handleMatchReport(self, matchReport):
        self.goals = {}
        clubX = list(matchReport['clubs'].keys())[0]   
        clubY = list(matchReport['clubs'].keys())[1]
        self.goals[clubX] = matchReport['clubs'][clubX]['match']['goalsFor']
        self.goals[clubY] = matchReport['clubs'][clubY]['match']['goalsFor']