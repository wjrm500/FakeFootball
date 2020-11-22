import numpy as np
from Player import Player
from Manager import Manager

class Club:
    def __init__(self):
        self.squad = []
        self.numReservesSelected = 0
        self.addManager()
        self.addPlayers()
        self.conductInitialAppraisal()
        self.setFeatures()
        # self.setAttributes()
        # self.setMoreAttributes()

    def addManager(self):
        self.manager = Manager()
        self.manager.club = self

    def addPlayers(self):
        while len(self.squad) < 40:
            player = Player()
            if player.retired is False:
                self.squad.append(player)
                player.club = self
        self.squad = sorted(self.squad, key = lambda x: x.rating, reverse = True)

    def conductInitialAppraisal(self):
        self.firstTeam = self.manager.selectTeam()
        self.firstTeamPlayers = [select.player for select in self.firstTeam.selection]

    def setFeatures(self):
        self.features = {}

        ### Get strength
        self.features['strength'] = self.firstTeam.rating

        ### Get depth
        squadMinusFirstTeamPlayers = [player for player in self.squad if player not in self.firstTeamPlayers]
        secondStringTeam = self.manager.selectTeam(squad = squadMinusFirstTeamPlayers)
        self.features['depth'] = secondStringTeam.rating / self.firstTeam.rating
    
    def addFutureVersion(self, futureVersion):
        self.squad.append(futureVersion)
        self.squad = sorted(self.squad, key = lambda x: x.rating, reverse = True)
        self.squad.pop()

    # def setAttributes(self):
    #     attributes = {}

    #     ### Get strength
    #     attributes['strength'] = self.firstTeam.rating

    #     ### Get depth
    #     squadMinusFirstTeamPlayers = [player for player in self.squad if player not in self.firstTeamPlayers]
    #     secondStringTeam = self.manager.selectTeam(squad = squadMinusFirstTeamPlayers)
    #     attributes['depth'] = secondStringTeam.rating / self.firstTeam.rating
            
    #     ### Get diversity
    #     attributes['diversity'] = np.mean([player.getDiversity() for player in self.squad])

    #     self.attributes = attributes
    
    # def setMoreAttributes(self):
    #     self.attributes['formation'] = self.manager.favouriteFormation
    #     playerRatings = [player.rating for player in self.squad]
    #     self.attributes['squadRatingsMean'] = np.mean(playerRatings)
    #     self.attributes['squadRatingsMedian'] = np.mean(playerRatings)
    #     self.attributes['squadRatingsStDev'] = np.std(playerRatings)
    #     for i in range(40):
    #         self.attributes['bestPlayer' + str(i)] = playerRatings[i]
    #     for position in ['CF', 'WF', 'COM', 'WM', 'CM', 'CDM', 'WB', 'FB', 'CB']:
    #         self.attributes['best' + position] = sorted(
    #             self.squad,
    #             key = lambda x: x.positionRatings[position],
    #             reverse = True
    #         )[0].positionRatings[position]
    #     for skill in ['offence', 'spark', 'technique', 'defence', 'authority', 'fitness']:
    #         self.attributes[skill] = np.mean([player.skillValues[skill] for player in self.squad])