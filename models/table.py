import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../validation/'))
from Validation import Validate
class table:
    def __init__(self, name, fields):
        self.name = name
        self.id = name
        self.fields = fields
        self.rows = []
    def updateRows(self, _rows):
        rows = []
        for (i, r) in enumerate(_rows):
            dict = {}
            for (j,f) in enumerate(self.fields):
                val = r[f.name]['value'].get()
                v = Validate(r[f.name]['type'])
                if(v.Validate(val) == True):
                    dict[f.name] = val
                else:
                    return False
            rows.append(dict)
        self.rows = rows