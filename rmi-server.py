from Pyro5.api import expose, Daemon
from databaseManager import databaseManager
from models.database import *

db = database("db1")

daemon = Daemon()
uri = daemon.register(databaseManager)
print("URI:", uri)
daemon.requestLoop()