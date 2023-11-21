from ariadne import convert_kwargs_to_snake_case
from databaseManager import databaseManager
from DictObjConvertor import *


def create_database_resolver(self, info, name):
    try:
        db = databaseManager.addDatabase(name)
        payload = {
            "success": True,
            "database": db
        }
    except Exception:  # date format errors
        payload = {
            "success": False,
            "errors": [Exception]
        }
    return payload

import jsonpickle
import json

def import_database_resolver(self, info, name):
    try:
        db = databaseManager.open(name)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        j = 0
        for t in db.tables:
            i = 0
            for r in t.rows:
                #r = toObjects(r)
                r = json.dumps(r, indent = 3) 
                t.rows[i] = r
                i += 1
            db.tables[j] = t
            j += 1

        print(jsonpickle.encode(db))
            
        payload = {
            "success": True,
            "database": db
        }
    except Exception:  # date format errors
        payload = {
            "success": False,
            "errors": [Exception]
        }
    return payload


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def jsonParse(dict):
   str = dict
   res = Struct(**str)
   return res


def create_table_resolver(self, info, db, tb):
    try:
        tb = jsonParse(tb)
        tb = databaseManager.postTable(db,tb)

        payload = {
            "success": True,
            "table": tb
        }
    except Exception:  # date format errors
        payload = {
            "success": False,
            "errors": ["error"]
        }
    return payload

def update_table_resolver(self, info, db, tb, rows):
    try:
        rows = toObjects(rows)
        databaseManager.updateRows(db,tb,rows)
        table = databaseManager.getTable(db,tb)
        table.rows = toDict(table.rows)
        payload = {
            "success": True,
            "table": table
        }
    except Exception:  # date format errors
        payload = {
            "success": False,
            "errors": [Exception]
        }
    return payload

def intersect_tables_resolver(self, info, db, tb1, tb2):
    try:
        tb = databaseManager.intersectTables(db,tb1,tb2)
        payload = {
            "success": True,
            "table": tb
        }
    except Exception:  # date format errors
        payload = {
            "success": False,
            "errors": [Exception]
        }
    return payload