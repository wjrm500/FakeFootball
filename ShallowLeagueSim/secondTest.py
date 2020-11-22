from Club import Club
from Manager import Manager

numLeagues = 2
numClubsPerLeague = 16
numPlayersPerClub = 20

league = [League() for i in range(numLeagues)]
for league in leagues:
    clubs = [Club() for i in range(numClubsPerLeague)]
    league.populateWithClubs(clubs)


for league in leagues:
    for club in league.clubs:
        club.scout()