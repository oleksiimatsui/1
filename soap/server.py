from spyne import Application, rpc, ServiceBase, Integer, Unicode, AnyDict, ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

from models.field import field
from databaseManager import databaseManager


class FieldModel(ComplexModel):
    name = Unicode
    type = Unicode
    default = Unicode


class RowModel(ComplexModel):
    values = Array(AnyDict)


class TableModel(ComplexModel):
    name = Unicode
    fields = Array(FieldModel)
    rows = Array(Unicode)


class DatabaseModel(ComplexModel):
    name = Unicode
    tables = Array(TableModel)


db_manager = databaseManager


class DBManagerService(ServiceBase):
    @rpc(_returns=Unicode)
    def get_database_name(self):
        return db_manager.db.name

    @rpc(_returns=Array(TableModel))
    def get_database_tables(self):
        return db_manager.db.tables

    @rpc(Unicode, _returns=DatabaseModel)
    def create_database(self, name):
        db_manager.create_database(name)
        db = db_manager.db
        print(f"Створено базу даних {name}")
        return DatabaseModel(name=db.name, tables=[])

    @rpc(Unicode, _returns=TableModel)
    def add_table(self, name):
        db_manager.add_table(name)
        table = db_manager.get_table(name)
        print(f"Створено таблицю {name}")
        return TableModel(name=table.name, columns=[], rows=[])

    @rpc(Unicode, _returns=TableModel)
    def get_table(self, name):
        table = db_manager.get_table(name)
        return TableModel(name=table.name,
                          columns=[FieldModel(type=col.type, name=col.name, default=col.default) for col in
                                   table.columns], rows=[RowModel(values=row.values) for row in table.rows])

    @rpc(Unicode, _returns=None)
    def delete_table(self, name):
        db_manager.delete_table(name)
        print(f"Видалено таблицю {name}")

    @rpc(Unicode, FieldModel, _returns=None)
    def add_column(self, table_name, column):
        col = FieldModel(column.type, column.name, column.default)
        db_manager.add_column(table_name, col)
        print(f"Додано атрибут {column.name} до таблиці {table_name}")

    @rpc(Unicode, AnyDict, _returns=None)
    def add_row(self, table_name, data):
        db_manager.add_row(table_name, data)
        print(f"Додано рядок до таблиці {table_name}")

    @rpc(Unicode, Integer, AnyDict, _returns=None)
    def change_row(self, table_name, index, data):
        db_manager.change_row(table_name, index, data)
        print(f"Змінено рядок таблиці {table_name}")

    @rpc(Unicode, Unicode, Unicode, _returns=TableModel)
    def join_tables(self, first_table_name, second_table_name, field_name):
        table = db_manager.join_tables(first_table_name, second_table_name, field_name)
        print(f"Сполучено таблиці {first_table_name} і {second_table_name} за спільним полем {field_name}")
        return TableModel(name=table.name,
                          columns=[FieldModel(type=col.type, name=col.name, default=col.default) for col in
                                   table.columns], rows=[RowModel(values=row.values) for row in table.rows])

    @rpc(Unicode, Integer, _returns=None)
    def delete_row(self, table_name, index):
        db_manager.delete_row(table_name, index)
        print(f"Вилучено рядок таблиці {table_name}")

    @rpc(Unicode, _returns=Unicode)
    def save_database(self, path_to_save):
        print(f"Збережено базу даних за шляхом {path_to_save}")
        return db_manager.save_database(path_to_save)

    @rpc(Unicode, _returns=None)
    def open_database(self, path_to_load):
        db_manager.open_database(path_to_load)
        print(f"Завантажено базу даних за шляхом {path_to_load}")


application = Application([DBManagerService],
                          tns='my.namespace',
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