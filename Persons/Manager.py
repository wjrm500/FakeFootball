import sys
sys.path.append('.')
from Persons.Person import Person
from operator import attrgetter
from config import playerConfig, managerConfig
import numpy as np
import Utilities.Utils as Utils
import copy
from Team import Team

class Manager(Person):
    def __init__(self, name = None, config = None):
        super(Manager, self).__init__(name)
        self.config = copy.deepcopy(managerConfig)
        if config is not None:
            Utils.updateConfig(self.config, config)
        self.club = None
        self.favouriteFormation = self.setFavouriteFormation()

    def selectTeam(self, squad = None):
        squad = self.club.squad if squad is None else squad
        chosenFormation = self.favouriteFormation
        personnelRequired = copy.deepcopy(self.config['formations'][chosenFormation]['personnel'])
        teamSelected = []
        while sum(personnelRequired.values()) > 0:
            maxValue = 0
            for position, numPlayers in personnelRequired.items():
                if numPlayers > 0:
                    for player in squad:
                        if player.injured is False and player.selected is False:
                            if player.positionRatings[position] > maxValue:
                                maxValue = player.positionRatings[position]
                                selection = {'position': position, 'player': player}
            selectedPosition = selection['position']
            selectedPlayer = selection['player']
            personnelRequired[selectedPosition] -= 1
            selectedPlayer.selected = True
            teamSelected.append(selection)
        for selection in teamSelected:
            selection['player'].selected = False
        return Team(self, chosenFormation, teamSelected)

    def setFavouriteFormation(self):
        formations, weights = [], []
        for key, value in self.config['formations'].items():
            formations.append(key)
            weights.append(value['popularity'])
        return np.random.choice(formations, size = 1, p = weights)[0]
    
    def printSelectedTeam(self, teamSelected):
        print(self.favouriteFormation)
        print('\n')
        print('THE SELECTED...')
        for selection in teamSelected:
            print(
                '{} - {:3} - Pos. Rating: {} - Best Pos.: {:3} - Best Pos. Rating: {}'.format(
                    selection['player'].name,
                    selection['position'],
                    int(selection['player'].positionRatings[selection['position']]),
                    selection['player'].bestPosition,
                    int(selection['player'].positionRatings[selection['player'].bestPosition])
                )
            )
        print('\n')
        print('THE UNSELECTED...')
        for player in sorted(self.club.squad, key = lambda x: x.positionRatings[x.bestPosition], reverse = True):
            if player.selected is False:
                print(
                    '{} - Best Pos.: {:3} - Best Pos. Rating: {}'.format(
                        player.name,
                        player.bestPosition,
                        int(player.positionRatings[player.bestPosition])
                    )
                )