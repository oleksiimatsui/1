class Row:
    def __init__(self, key, value):
        self.key = str(key)
        self.value = str(value)

def toDict(objects):
    res = {}
    for o in objects:
        res[str(o.key)] = str(o.value)
    return res

def toObjects(dict):
    list = []
    print(dict)
    for key,value in dict.items():
       list.append(Row(key,value))
    return list