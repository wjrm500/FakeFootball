from TimeLord import TimeLord
import pickle
from datetime import datetime

print(datetime.now())
timeLord = TimeLord(1900, 2000)
timeLord.createUniverse()
timeLord.timeTravel(300)
division = timeLord.Universe.systems[0].divisions[0]
division.displayLeagueTable()
division.displayPlayerStats(stat = 'goals', numRecords = 100)