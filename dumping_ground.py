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