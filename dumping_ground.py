# team1 = Team()
testManager = Manager()
# for i in range(40):
#     team1.signPlayer(Player())
# team1.hireManager(testManager)

# for player in team1.squad:
#     print(player.name, ":", player.bestPosition)

# testManager.selectTeam(team1.squad)

favouriteFormationInstances = []
for i in range(2_500):
    manager = Manager()
    shortPriorities = {key[0]: round(value, 3) for key, value in manager.priorities.items()}
    favouriteFormationInstances.append(manager.favouriteFormation)

from collections import Counter
print(Counter(favouriteFormationInstances))

formationSkills = {}
for formation in managerConfig['formations']:
    formationSkills[formation['name']] = {skill: 0 for skill in playerConfig['skill']['skills']}
    for position, numPlayers in formation['personnel'].items():
        for i in range(numPlayers):
            for skill, value in playerConfig['positions'][position]['skillDistribution'].items():
                formationSkills[formation['name']][skill] += (value / 10)

# for formation, fSkills in formationSkills.items():
#     shortFSkills = {key[0]: round(value, 3) for key, value in fSkills.items()}
#     print(formation, shortFSkills)

# skillWeightings = {}
# for formation, fSkills in formationSkills.items():
#     for skill, value in fSkills.items():
#         for configFormation in managerConfig['formations']:
#             if configFormation['name'] == formation:
#                 skillWeightings[skill] = value * configFormation['popularity']

# totalSkillWeighting = sum(skillWeightings.values())
# for key, value in skillWeightings.items():
#     skillWeightings[key] = value * len(skillWeightings) / totalSkillWeighting

# print(skillWeightings)

    # def setFavouriteFormation(self):
    #     formationSkills = {}
    #     for formation in managerConfig['formations']:
    #         formationSkills[formation['name']] = {skill: 0 for skill in playerConfig['skill']['skills']}
    #         for position, numPlayers in formation['personnel'].items():
    #             for i in range(numPlayers):
    #                 for skill, value in playerConfig['positions'][position]['skillDistribution'].items():
    #                     formationSkills[formation['name']][skill] += (value / 10)

    #     formationIncompatibilities = {}
    #     for formation, fSkills in formationSkills.items():
    #         incompatibility = 0
    #         for skill, value in fSkills.items():
    #             incompatibility += abs(value - self.priorities[skill])
    #         formationIncompatibilities[formation] = incompatibility
        
    #     favouriteFormation = min(formationIncompatibilities, key = formationIncompatibilities.get)
    #     return favouriteFormation

    
# showSkillDistribution([selection['player'] for selection in matchEngine.homeTeam])
# showSkillDistribution([selection['player'] for selection in matchEngine.awayTeam])

# h = matchEngine.homeTeamSkills
# a = matchEngine.awayTeamSkills

# homeBoost, awayBoost = 0, 0
# for k, v in h.items():
#     if k not in ['offence', 'defence']:
#         diff = v - a[k]
#         if diff > 0:
#             homeBoost += (diff / 100) ** 1.1
#         elif diff < 0:
#             diff *= -1
#             awayBoost += (diff / 100) ** 1.1

# homeOffencePotential = matchEngine.homeTeamSkills['offence'] - matchEngine.awayTeamSkills['defence']
# awayOffencePotential = matchEngine.awayTeamSkills['offence'] - matchEngine.homeTeamSkills['defence']

# print(
#     '{}\n{}\n{}\n{}'.format(
#         'Home team:',
#         matchEngine.homeClub.name, 
#         matchEngine.homeClub.manager.favouriteFormation,
#         {skill: int(value) for skill, value in matchEngine.homeTeamSkills.items()}
#     )
# )
# print('Home boost:', homeBoost)
# print('Home offence potential:', homeOffencePotential)
# print('Home offence potential with boost:', homeOffencePotential + abs(homeOffencePotential * homeBoost))
# print('\n')
# print(
#     '{}\n{}\n{}\n{}'.format(
#         'Away team:',
#         matchEngine.awayClub.name, 
#         matchEngine.awayClub.manager.favouriteFormation,
#         {skill: int(value) for skill, value in matchEngine.awayTeamSkills.items()}
#     )
# )
# print('Away boost:', awayBoost)
# print('Away offence potential:', awayOffencePotential)
# print('Away offence potential with boost:', awayOffencePotential + abs(awayOffencePotential * awayBoost))

#################

clubs = []
for i in range(2):
    club = Club()
    while len(club.squad) < 40:
        player = Player()
        if player.retired is False:
            club.signPlayer(player)
    club.hireManager(Manager())
    clubs.append(club)

matchEngine = MatchEngine(clubs[0], clubs[1])
for club in matchEngine.clubs.values():
    print(club)
    print(club.team.offence)
    print(club.team.defence)
    print('\n')
print(matchEngine.potentials)
print('\n')
result = matchEngine.playMatch()
print(result)

### Assigning names to pickled TimeLord players
i = 0
for system in timeLord.Universe.systems:
    for division in system.divisions:
        for club in division.clubs:
            for player in club.squad:
                player.name = Utils.generatePlayerName()
                i += 1
                print(i)

outfile = open('timeLord', 'wb')
pickle.dump(timeLord, outfile)
outfile.close()
exit()

personController = PersonController()
player = personController.createPlayer(Player(personController, age = 15))
ages, ratings, peakRatings = [], [], []
retiredAlready = 0
for i in range(7300):
    ages.append(player.age)
    ratings.append(player.rating)
    peakRatings.append(player.peakRating)
    if player.retired is True and retiredAlready == 0:
        retiredAlready = 1
        ageAtRetirement = player.age
    personController.advance()

plt.plot(ages, peakRatings)
plt.plot(ages, ratings)
plt.axvline(x = ageAtRetirement, c = 'red', ls = '--')
plt.show()

    # def setAttributes(self):
    #     attributes = {skill: 0 for skill in playerConfig['skill']['skills']}
    #     for selection in self.teamSelected:
    #         player = selection['player']
    #         playerRating = self.getPlayerRatingFromSelection(selection)
    #         for skill, value in player.skillDistribution.items():
    #             attributes[skill] += (value * playerRating) / 10
    #     self.attributes = attributes
    
    # def setOffenceDefence(self):
    #     self.offence, self.defence = 0, 0
    #     for attributeKey in self.attributes.keys():
    #         self.offence += self.attributes[attributeKey] * matchConfig['contribution'][attributeKey]['offence']
    #         self.defence += self.attributes[attributeKey] * matchConfig['contribution'][attributeKey]['defence']
    #     self.offence, self.defence = self.offence / 3, self.defence / 3

        def getBestPlayers(self, position):
        sortedPlayers = sorted(self.players, key = lambda x: x.rating, reverse = True)
        if position is not None:
            sortedPlayers = [player for player in sortedPlayers if player.bestPosition == position]
        return sortedPlayers
    
    def displayBestPlayers(self, position = None, numRecords = 5):
        x = self.getBestPlayers(position)
        for player in x[0:numRecords]:
            playerName = player.properName
            club = player.club.name
            ratPos = '{} rated {}'.format(str(int(round(player.rating))), player.bestPosition)
            numGoals = self.goalscorers.count(player)
            numAssists = self.assisters.count(player)
            print('Player: {:30} - {:12} - Club: {} - {:2} goals and {:2} assists'.format(playerName, ratPos, club, numGoals, numAssists))
    
     def getPlayerStats(self, stat):
        if stat == 'goals':
            l = self.goalscorers
        elif stat == 'assists':
            l = self.assisters
        x = [{'player': player, stat: l.count(player)} for player in set(l)]
        x = sorted(x, key = lambda k: k[stat], reverse = True)
        return x
    
    def displayPlayerStats(self, stat, numRecords):
        x = self.getPlayerStats(stat)
        for item in x[0:numRecords]:
            playerName = ' '.join(item['player'].properName)
            club = item['player'].club.name
            numItems = item[stat]
            ratPos = '{} rated {}'.format(str(int(round(item['player'].rating))), item['player'].bestPosition)
            print('Player: {:30} - {:12} - Club: {} - {:2} {}'.format(playerName, ratPos, club, numItems, stat))

        
### This was in System

    # def displayTopScorersAssisters(self):
    #     for y, z in zip(
    #         [self.goalscorers, self.assisters, self.goalscorers + self.assisters],
    #         ['goals', 'assists', 'goals and assists']
    #         ):
    #         print('Top ranked players for {}:'.format(z))
    #         y = [{'player': player, z: y.count(player)} for player in set(y)]
    #         y = sorted(y, key = lambda x: x[z], reverse = True)
    #         for item in y[0:5]:
    #             playerName = item['player'].name
    #             club = item['player'].club.name
    #             numItems = item[z]
    #             ratPos = '{} rated {}'.format(str(int(round(item['player'].rating))), item['player'].bestPosition)
    #             if z in ['goals', 'assists']:
    #                 print('Player: {} - {} - Club: {} - {:2} {}'.format(playerName, ratPos, club, numItems, z))
    #             elif z == 'goals and assists':
    #                 numGoals = self.goalscorers.count(item['player'])
    #                 numAssists = self.assisters.count(item['player'])
    #                 print('Player: {} - {} - Club: {} - {:2} goals and {:2} assists'.format(playerName, ratPos, club, numGoals, numAssists))
    #         print('\n')

        ### Schedule dates
        currentDate = date(systemKnockout.year, 1, 1)
        while True:
            if year(currentDate) > year: ### Exit loop when year changes / when fixtures have been exhausted
                    return
            def lookForFixtures(currentDate):
                if currentDate.weekday() == 2:
                    for roundKey, roundValue in systemKnockout.fixtures.items():
                        if None in fixture['dates']: ### Is there at least one vacant slot in this fixture?
                            fixture['dates'][fixture['dates'].index(None)] = currentDate
                            return
            lookForFixtures(currentDate)
            currentDate += timedelta(days = 1)

        prelimTeams = systemKnockout.clubs[-32:] ### Get 32 lowest-rated teams
        nonPrelimTeams = systemKnockout.clubs[:-32] ### Get all other teams (who do not take part in preliminary round)
        ### Add preliminary teams to preliminary round
        for prelimTeam in prelimTeams:
            cls.updateSystemKnockoutFixtures(systemKnockout, prelimTeam)
        ### Add non-preliminary teams straight into Round of 64
        for nonPrelimTeam in nonPrelimTeams:
            cls.updateSystemKnockoutFixtures(systemKnockout, nonPrelimTeam)
    
    # @classmethod
    # def scheduleGlobalKnockoutFixtures(year, globalKnockout):
    #     pass
    
    @classmethod
    def updateSystemKnockoutFixtures(knockout, team):
        for roundKey, roundValue in systemKnockout.fixtures.items():
            fixtures = roundValue['fixtures']
            for fixture in fixtures:
                if None in fixture['clubs']: ### Is there at least one vacant slot in this fixture?
                    ### We have found the round we want to insert into. Now we need to insert into a random vacant position
                    randomFixtureIndex = random.choice([i for i, fixture in enumerate(fixtures) if None in fixture['clubs']])
                    randomSlotIndex = random.choice([i for i, slot in enumerate(fixture['clubs']) if slot is None])
                    systemKnockout.fixtures[roundKey]['fixtures'][randomFixtureIndex]['clubs'][randomSlotIndex] = team
                    return