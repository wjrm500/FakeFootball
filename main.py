from TimeLord import TimeLord
import pickle
from datetime import datetime
import Utilities.Utils as Utils

timeLord = TimeLord({
    'numSystems': 1,
    'numLeaguesPerSystem': 1,
    'numClubsPerLeague': 10,
    'numPersonnelPerClub': {
        'Player': 30
    }
})
timeLord.createUniverse()
i = 1
for system in timeLord.universe.systems:
    for club in system.clubs:
        club.setInternalScoutReports()
        club.setExternalScoutReports()
        print('Clubs completed:' + str(i))
        i += 1

# with open('dict44773', 'rb') as file:
#     internalScoutReports = pickle.load(file)

# with open('dict53703', 'rb') as file:
#     externalScoutReports = pickle.load(file)

with open('transferValueTest.txt', 'w', encoding = 'utf-8') as file:
    for scoutReports in [internalScoutReports, externalScoutReports]:
        for club, data in scoutReports.items():
            for player, valuations in data.items():
                file.write(','.join(
                    [
                        club.name,
                        str(club.getRating()),
                        player.properName,
                        player.club.name,
                        str(player.age),
                        str(player.rating),
                        str(player.peakAge),
                        str(player.peakRating),
                        player.getBestPosition(),
                        str(valuations['imperfect']),
                        str(valuations['perfect'])
                        ]
                    )
                )
                file.write('\r')
        file.write('\n' * 5)

# Utils.pickleObject(internalScoutReports)
# Utils.pickleObject(externalScoutReports)

try:
    Utils.pickleObject(timeLord)
except:
    Utils.pickleLargeObject(timeLord)

# timeLord.timeTravel(300)
# division = timeLord.Universe.systems[0].divisions[0]
# division.displayLeagueTable()
# division.displayPlayerStats(stat = 'goals', numRecords = 100)