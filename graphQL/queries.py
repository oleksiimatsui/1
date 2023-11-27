from ariadne import convert_kwargs_to_snake_case
from databaseManager import databaseManager
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from services.DictObjConvertor import *

def get_database_resolver(self, info, db):
    db = databaseManager.getDatabase(db)
    return db


def get_databases_resolver(self, info,):
    return databaseManager.getDatabases()

def get_tables_resolver(self,info,db):
    return databaseManager.getTables(db)

def get_table_resolver(self,info,db,tb):
    return databaseManager.getTable(db,tb)
