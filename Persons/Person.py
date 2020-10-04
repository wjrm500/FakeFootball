import sys
sys.path.append('.')
import Utilities.Utils as Utils

class Person:
    def __init__(self, name):
        self.name = Utils.generateName(10) if name is None else name