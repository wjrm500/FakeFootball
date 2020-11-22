import numpy as np
import collections.abc
import random
import string
import pickle
import os
import glob

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

def generateRandomDigits(n):
    return ''.join(random.choice(string.digits) for _ in range(n))

def pickleObject(obj):
    objName = type(obj).__name__ + str(generateRandomDigits(5))
    outfile = open(objName, 'wb')
    pickle.dump(obj, outfile)
    outfile.close()

def unpickleMostRecent(path):
    files = glob.glob(path + '/*')
    latestPickleFileName = max(files, key = os.path.getctime)
    latestPickle = open(latestPickleFileName, 'rb')
    latestPickleUnpickled = pickle.load(latestPickle)
    latestPickle.close()
    return latestPickleUnpickled