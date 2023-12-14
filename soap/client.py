import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

from databaseManager import databaseManager
from zeep import Client
soap_client = Client('http://localhost:8000/?wsdl')


soap_client.service.open_database("example1")
