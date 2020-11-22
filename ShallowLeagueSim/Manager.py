from Person import Person
from config import managerConfig
import numpy as np
import Utils
import copy
from Team import Team
from Select import Select

class Manager(Person):
    def __init__(
        self,
        config = None
        ):
        self.config = copy.deepcopy(managerConfig)
        if config is not None:
            Utils.updateConfig(self.config, config)
        self.club = None
        self.favouriteFormation = self.setFavouriteFormation()

    def setFavouriteFormation(self):
        formations, weights = [], []
        for key, value in self.config['formations'].items():
            formations.append(key)
            weights.append(value['popularity'])
        return np.random.choice(formations, size = 1, p = weights)[0]

    def selectTeam(self, homeAway = 'neutral', squad = None):
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
                                selectRating -= selectRating * player.fatigue
                                selectRating += (selectRating * player.form) / 10
                                if selectRating > maxValue:
                                    maxValue = selectRating
                                    select = Select(player, position, selectRating)
                personnelRequired[select.position] -= 1
                selection.append(select)
            return Team(self, chosenFormation, selection, homeAway)
        except:
            return None

