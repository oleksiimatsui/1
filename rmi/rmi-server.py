from Pyro5.api import expose, Daemon
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from databaseManager import databaseManager
from models.database import *

db = database("db1")

daemon = Daemon()
uri = daemon.register(databaseManager)
print("URI:", uri)
daemon.requestLoop()