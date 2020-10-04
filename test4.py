from TimeLord import TimeLord

timeLord = TimeLord(1900, 2000)
timeLord.createUniverse()
timeLord.timeTravel(150)
div = timeLord.systemController.systems[0].divisions[0]
div.displayLeagueTable()
div.displayTopScorersAssisters()
div.displayBestPlayers()