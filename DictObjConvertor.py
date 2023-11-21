class Row:
    def __init__(self, key, value):
        self.key = key
        self.value = value

def toDict(objects):
    res = {}
    for o in objects:
        print(o.key)
        res[o.key] = o.value
    return res

def toObjects(dict):
    list = []
    print(dict)
    for key,value in dict.items():
       list.append(Row(key,value))
    return list