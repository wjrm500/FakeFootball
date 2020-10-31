from Tournaments.Group import Group
from TournamentStage import TournamentStage
import random

class GroupStage(TournamentStage):
    def __init__(self, tournament, stage = 'Group Stage'):
        super().__init__(tournament, stage)
        numGroups = 8 if type(tournament).__name__ == 'SuperiorUniversalTournament' else 12
        self.groups = {chr(i + 65): Group(self.tournament) for i in range(numGroups)}
        for key, group in self.groups.items():
            group.populateWithClubs([{'{}{}'.format(key, i + 1): None} for i in range(4)]) ### Placeholders

    def draw(self, clubs):
        random.shuffle(clubs)
        for club in clubs:
            availableGroups = [group for group in self.groups.values() if group.getNumPlaceholders() > 0]
            randomlySelectedGroup = random.choice(availableGroups)
            randomlySelectedGroup.replacePlaceholderWithClub(club)

    def checkNewlyComplete(self):
        if self.complete == False and all([group.checkComplete() for group in self.groups.values()]):
            self.complete = True
            return True
        
    def setProgressors(self):
        if type(self.tournament).__name__ == 'SuperiorUniversalTournament':
            self.progressors = {
                'firsts': [],
                'seconds': []
            }
            for group in self.groups.values():
                self.progressors['firsts'].append(group.getClubByRank(0))
                self.progressors['seconds'].append(group.getClubByRank(1))
        elif type(self.tournament).__name__ == 'InferiorUniversalTournament':
            self.progressors = []
            for group in self.groups.values():
                for rank in [0, 1]:
                    self.progressors.append(group.getClubByRank(rank))
    
    def setDropouts(self):
        self.tournament.dropouts = []
        for key, group in self.groups.items():
            self.tournament.dropouts.append(group.getClubByRank(2))