import random
import string
import collections.abc
import numpy as np

def generateName(chars):        
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(chars))

def limitValue(value, mn, mx):
    if value < mn:
        return mn
    elif value > mx:
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