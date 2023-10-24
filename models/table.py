import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../validation/'))
from Validation import Validate
class table:
    def __init__(self, name, fields):
        self.name = name
        self.id = name
        self.fields = fields
        self.rows = []

    def validate(self, _rows):
        for (i, r) in enumerate(_rows):
            for (j,f) in enumerate(self.fields):
                val = r[f.name]
                v = Validate(f.type)
                if(v.Validate(val) != True):
                    return False
        return True

    def updateRows(self, rows):
        if(self.validate(rows) == False):
            return False
        self.rows = rows