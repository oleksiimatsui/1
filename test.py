# test_with_pytest.py
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'models/'))
from databaseManager import databaseManager
from table import table
from field import field

def test_intersection():
    databaseManager.addDatabase("new DB")
    db = databaseManager.databases[0]
    fields = []
    fields.append(field("char", "Char"))
    t1 = table("t1", fields)
    t2 = table("t2", fields[:])
    db.addTable(t1)
    db.addTable(t2)
    t1.rows = [{"char": "a"}, {"char": "c"}]
    t2.rows = [{"char": "a"}, {"char": "b"}]
    db.intersect([t1, t2])
    t3 = db.tables[2]
    rows = t3.rows
    if(rows == [{"char": "a"}]):
        assert True
        return
    assert False


def test_char():
    databaseManager.addDatabase("new DB")
    db = databaseManager.databases[0]
    fields = []
    fields.append(field("char", "Char"))
    t1 = table("t1", fields)
    rows = [{"char": "name"}]
    res = t1.updateRows(rows)
    if(res == True):
        assert False
    else:
        assert True

def test_moneyInterval():
    databaseManager.addDatabase("new DB")
    db = databaseManager.databases[0]
    fields = []
    fields.append(field("MI", "MoneyInterval"))
    t1 = table("t1", fields)
    rows = [{"MI": "12.2,13.1"}]
    res = t1.updateRows(rows)
    if(res == False):
        assert False
    else:
        assert True