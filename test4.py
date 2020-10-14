from Club import Club
import Utilities.Utils as Utils

d = {
    'date': 'stuff',
    Club(): 'stuff',
    Club(): 'stuff'
}

print([id(key) for key in d.keys()])
x = Utils.typeAgnosticOmit(d, 'date')
print([id(key) for key in x.keys()])