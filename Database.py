import mysql.connector

class Database:

    __instance__ = None

    def __init__(self):
        if Database.__instance__ is None:
            Database.__instance__ = self
            self.connect()
        else:
            raise Exception("You cannot create another Database class")

    @staticmethod
    def getInstance():
        if not Database.__instance__:
            Database()
        return Database.__instance__
    
    def connect(self):
        self.cnx = mysql.connector.connect(
            user = 'root',
            password = 'Gigabit123',
            host = '127.0.0.1',
            database = 'fakefootball'
        )
        self.cursor = self.cnx.cursor(dictionary = True)
