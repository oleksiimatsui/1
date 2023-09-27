from table import table
from field import field
import pickle

class database:
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
        self.tables.append(table(_t.name, fields))
        return True

    def deleteTable(self, id):
        for i, db in enumerate(self.tables):
            if(db.id == id):
                self.tables.remove(db)
                return
    def addTable(self, table):
        self.tables.append(table)
    def getTables(self):
        return self.tables
    
    def save_object(self, file):
        with open(file, 'wb') as outp:  # Overwrites any existing file.
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
        self.tables.append(t)