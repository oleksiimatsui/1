from concurrent import futures
import grpc
import pickle
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from databaseManager import databaseManager
import dbm_pb2_grpc
import dbm_pb2
import socket


class DatabaseManagerService(dbm_pb2_grpc.DatabaseManagerServicer):
    def __init__(self):
        self.db_manager = databaseManager()

    def OpenDatabase(self, request, context):
        db = self.db_manager.open(request.name)
        return dbm_pb2.Database(name=db.name, tables=self._tables_to_proto(db.tables))
    
    def IntersectTables(self, request, context):
        tb = self.db_manager.intersectTables(request.db, request.tb1, request.tb2)
        return self._table_to_proto(tb)
    
    def _tables_to_proto(self,tables):
        proto_tables = []
        for table in tables:
            proto_tables.append(self._table_to_proto(table))
        return proto_tables
    
    def _table_to_proto(self, table):
        proto_table = dbm_pb2.Table(id = table.id, name=table.name)
        for field in table.fields:
            proto_table.fields.append(self._field_to_proto(field))
        for row in table.rows:
            proto_table.rows.append(self._row_to_proto(row))
        return proto_table
    
    def _field_to_proto(self, column):
        return dbm_pb2.Field(
            name=column.name,
            type=column.type,
        )

    def _row_to_proto(self, row):
        proto_row = dbm_pb2.Row(values = [])
        for (key,value) in row.items():
            proto_row.values.append(dbm_pb2.KeyValue(key = key, value = value))
        return proto_row


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dbm_pb2_grpc.add_DatabaseManagerServicer_to_server(DatabaseManagerService(), server)
    server_address = '[::]:50051'
    server.add_insecure_port(server_address)
    port = server_address.split(':')
    ip_address = socket.gethostbyname(socket.gethostname())
    print(f'Server is listening on http://{ip_address}:{port[3]}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()