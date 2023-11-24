from concurrent import futures
import grpc
import pickle

from databaseManager import databaseManager


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dbmanager_pb2_grpc.add_DatabaseManagerServicer_to_server(DatabaseManagerService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Сервер працює на порті 50051...')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()