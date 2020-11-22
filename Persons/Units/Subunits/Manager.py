import sys
sys.path.append('.')
from Persons.Units.Person import Person
from operator import attrgetter
import numpy as np
import Utilities.Utils as Utils
import copy
from Team import Team
from Select import Select

class Manager(Person):
    ### TODO: Managers to have ratings that determine how good they are picking their team among other things
    ### TODO: Greater flexibility in choosing formations based on attributes of squad
    ### TODO: Manager - player relationships - Grows over time, weakens by not selecting player, grows by team overperformance

    def __init__(
        self,
        controller,
        id,
        config = None,
        name = None
        ):
        super(Manager, self).__init__(controller, id, config, name)
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
            if len(squad) < 10:
                raise Exception('Not enough players to form a full team.')
            chosenFormation = self.favouriteFormation
            personnelRequired = copy.deepcopy(self.config['formations'][chosenFormation]['personnel'])
            selection = []
            while sum(personnelRequired.values()) > 0:
                maxValue = 0
                for position, numPlayers in personnelRequired.items():
                    if numPlayers > 0:
                        for player in squad:
                            if player not in [select.player for select in selection] and player.injured is False:
                                selectRating = player.futureVersion['positionRatings'][position] if hasattr(player, 'futureVersion') else player.positionRatings[position]
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