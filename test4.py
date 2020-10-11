from PersonController import PersonController
from Persons.Player import Player
from datetime import date
import matplotlib.pyplot as plt

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