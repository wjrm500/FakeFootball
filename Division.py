from Team import Team

class Division:
    def __init__(self, systemConfig):
        self.teams = [Team() for _ in range(systemConfig['numTeamsPerDivision'])]