import random, string

def generateName(name, chars):        
    if name is None:
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(chars))
    else:
        return name