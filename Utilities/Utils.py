import random
import string
import collections.abc
import numpy as np
import random
from datetime import date
from dateutil.relativedelta import relativedelta
import mysql.connector
import copy

cnx = mysql.connector.connect(user = "root",
                              password = "Gigabit123",
                              host = "127.0.0.1",
                              database = "simulator")

def generateName(chars):        
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(chars))

def loadPlayerNames():
    cursor = cnx.cursor()
    get_firstname = 'SELECT firstname, `count` FROM fakefootball.firstnames'
    cursor.execute(get_firstname)
    resultSet = cursor.fetchall()
    global forenames, forenameWeights
    forenames = [record[0] for record in resultSet]
    forenameWeights = [record[1] for record in resultSet]
    forenameWeights = [forenameWeight / sum(forenameWeights) for forenameWeight in forenameWeights]
    get_surname = 'SELECT surname, `count` FROM fakefootball.surnames'
    cursor.execute(get_surname)
    resultSet = cursor.fetchall()
    global surnames, surnameWeights
    surnames = [record[0] for record in resultSet]
    surnameWeights = [record[1] for record in resultSet]
    surnameWeights = [surnameWeight / sum(surnameWeights) for surnameWeight in surnameWeights]
    cursor.close()

def generatePlayerName():
    if 'forenames' not in globals():
        loadPlayerNames()
    forename = np.random.choice(forenames, p = forenameWeights)
    surname = np.random.choice(surnames, p = surnameWeights)
    return (forename, surname)

def limitValue(value, mn = None, mx = None):
    if mn is not None:
        if value < mn:
            return mn
    if mx is not None:
        if value > mx:
            return mx
    return value

def limitedRandNorm(dictionary):
    [mu, sigma, mn, mx] = [value for value in list(dictionary.values())]
    return limitValue(np.random.normal(mu, sigma), mn, mx)

def updateConfig(existingConfig, newConfig):
    for key, value in newConfig.items():
        if isinstance(value, collections.abc.Mapping):
            existingConfig[key] = updateConfig(existingConfig.get(key, {}), value)
        else:
            existingConfig[key] = value
    return existingConfig

def getBirthDate(dateCreated, age):
    startDate = dateCreated - relativedelta(years = age + 1) + relativedelta(days = 1)
    endDate = dateCreated - relativedelta(years = age)
    ordinalStartDate = startDate.toordinal()
    ordinalEndDate = endDate.toordinal()
    randomOrdinalDate = random.randint(ordinalStartDate, ordinalEndDate)
    randomDate = date.fromordinal(randomOrdinalDate)
    return randomDate

def typeAgnosticOmit(dictionary, omittedKeys):
    """Omits given keys from dictionary."""
    output = copy.deepcopy(dictionary)
    omittedKeys = omittedKeys if type(omittedKeys) == list else [omittedKeys]
    for omittedKey in omittedKeys:
        try:
            del output[omittedKey]
        except:
            continue
    return output