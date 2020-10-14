import sys
sys.path.append('.')
from Persons.Person import Person
from operator import attrgetter
from config import playerConfig, managerConfig
import numpy as np
import Utilities.Utils as Utils
import copy
from Team import Team
from Select import Select

class Manager(Person):
    def __init__(
        self,
        personController,
        id,
        name = None,
        config = None
        ):
        super(Manager, self).__init__(personController, id, name)
        self.config = copy.deepcopy(managerConfig)
        if config is not None:
            Utils.updateConfig(self.config, config)
        self.club = None
        self.favouriteFormation = self.setFavouriteFormation()

    def selectTeam(self, squad = None):
        try:
            squad = self.club.squad if squad is None else squad
            chosenFormation = self.favouriteFormation
            personnelRequired = copy.deepcopy(self.config['formations'][chosenFormation]['personnel'])
            selection = []
            while sum(personnelRequired.values()) > 0:
                maxValue = 0
                for position, numPlayers in personnelRequired.items():
                    if numPlayers > 0:
                        for player in squad:
                            if player not in [select.player for select in selection] and player.injured is False:
                                selectRating = player.positionRatings[position]
                                selectRating = selectRating - (selectRating * player.fatigue)
                                if selectRating > maxValue:
                                    maxValue = selectRating
                                    select = Select(player, position)
                selectPlayer = select.player
                selectPosition = select.position
                personnelRequired[selectPosition] -= 1
                selection.append(select)
            for select in selection:
                selectPlayer.selected = False
            return Team(self, chosenFormation, selection)
        except:
            return None

    def setFavouriteFormation(self):
        formations, weights = [], []
        for key, value in self.config['formations'].items():
            formations.append(key)
            weights.append(value['popularity'])
        return np.random.choice(formations, size = 1, p = weights)[0]
    
    def printSelectedTeam(self, selection):
        print(self.favouriteFormation)
        print('\n')
        print('THE SELECTED...')
        for select in selection:
            print(
                '{} - {:3} - Pos. Rating: {} - Best Pos.: {:3} - Best Pos. Rating: {}'.format(
                    select.player.name,
                    select.position,
                    int(select.player.positionRatings[select.position]),
                    select.player.bestPosition,
                    int(select.player.positionRatings[select.player.bestPosition])
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