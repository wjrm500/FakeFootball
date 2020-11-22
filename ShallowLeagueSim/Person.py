import random

class Person:
    def __init__(self):
        self.setAge()
        self.retired = False
    
    def setAge(self):
        self.age = random.uniform(15, 40)