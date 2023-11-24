

from models.field import field
from models.table import table
import pickle
from Pyro5.api import expose

@expose
class database:

    TABLES_IK = 0

    def __init__(self, name):
        self.tables = []
        self.isSaved = False
        self.name = name
        self.id = name
        self.file = ''

    
    def addTableFromPseudo(self, _t):
        fields = []
        for f in _t.fields:
            name = f["name"].get()
            type = f["type"].get()
            if(name == "" or type == ""):
                return False
            fields.append(field(name, type))
        if(fields != list(set(fields))):
            return False
        if(_t.name == ''):
            return False
        self.addTable(table(_t.name, fields))
        return True

    def deleteTable(self, id):
        for i, db in enumerate(self.tables):
            if(db.id == id):
                self.tables.remove(db)
                return
    def addTable(self, table):
        database.TABLES_IK += 1
        table.id = database.TABLES_IK
        self.tables.append(table)
    
    def getTables(self):
        return self.tables

    def getTable(self,id):
        for x in self.tables:
            if str(x.id) == str(id):
                return x
        return "not found"
    
    def save_object(self, file):
        with open("files/"+file, 'wb') as outp:  # Overwrites any existing file.
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)

    def save(self, name):
        self.isSaved = True
        self.file = name
        self.save_object(name)
    def intersect(self,list):
        if len(list) != 2:
            return False
        t1 = list[0]
        t2 = list[1]
        name = t1.name + "_" + t2.name + "_intersection"
        for i, f in enumerate(t1.fields):
            f2 = t2.fields[i]
            if(f.name != f2.name or f.type != f2.type):
                return False

        t = table(name, t1.fields)
        rows = [value for value in t1.rows if value in t2.rows]
        t.rows = rows
        self.addTable(t)
        return t