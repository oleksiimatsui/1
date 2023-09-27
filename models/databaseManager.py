import pickle
from database import database

class databaseManager():
    databases = []
    @staticmethod
    def addDatabase(name):
        d = database(name)
        databaseManager.databases.append(d)
    @staticmethod
    def deleteDatabase(id):
        for i, db in enumerate(databaseManager.databases):
            if(db.id == id):
                databaseManager.databases.remove(db)
                return 
    @staticmethod
    def open(name):
        with open(name, 'rb') as inp:
            db = pickle.load(inp)
        databaseManager.databases.append(db)
    