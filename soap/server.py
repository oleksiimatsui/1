from spyne import Application, rpc, ServiceBase, Integer, Unicode, AnyDict, ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

from databaseManager import databaseManager


class FieldModel(ComplexModel):
    name = Unicode
    type = Unicode

class RowModel(ComplexModel):
    values = Array(AnyDict)

class TableModel(ComplexModel):
    id = Integer
    name = Unicode
    fields = Array(FieldModel)
    rows = Array(AnyDict)

class DatabaseModel(ComplexModel):
    id = Unicode
    name = Unicode
    tables = Array(TableModel)


class DBManagerService(ServiceBase):
    @rpc(_returns=Array(DatabaseModel))
    def get_database(self):
        db = databaseManager.getDatabases()
        return db

    @rpc(Unicode, _returns=DatabaseModel)
    def get_database(self, name):
        db = databaseManager.getDatabase(name)
        return db
    
    @rpc(Unicode, _returns=Array(TableModel))
    def get_tables(self, db):
        return databaseManager.getTables(db)

    @rpc(Unicode, _returns=DatabaseModel)
    def create_database(self, name):
        databaseManager.addDatabase(name)
        db = databaseManager.db
        return db

    @rpc(Unicode, Unicode, _returns=TableModel)
    def add_table(self, db, name):
        tb = databaseManager.postTable(db,name)
        return tb

    @rpc(Unicode, Integer, _returns=TableModel)
    def get_table(self, db, tb):
        table = databaseManager.getTable(db, tb)
        return table

    @rpc(Unicode, Integer, _returns=None)
    def delete_table(self, db, tb):
        databaseManager.deleteTable(db,tb)

    @rpc(Unicode, _returns=None)
    def save_database(self, name):
        return databaseManager.save(name)

    @rpc(Unicode, _returns=DatabaseModel)
    def open_database(self, name):
        db = databaseManager.open(name)
        print(db)
        return db
    @rpc(Unicode, Integer, Integer, _returns=TableModel)
    def intersect(self, db, tb1, tb2):
        return databaseManager.intersectTables(db,tb1,tb2)



application = Application([DBManagerService],
                          tns='db.namespace',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    host = '127.0.0.1'
    port = 8000
    print(f"Сервер працює на {host}:{port}")
    server = make_server(host, port, wsgi_application)
    server.serve_forever()