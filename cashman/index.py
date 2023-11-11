import jsonpickle
from flask import Flask
from flask import render_template
from flask import request
from flasgger import Swagger
from flasgger import swag_from
app = Flask(__name__)
swagger = Swagger(app)
import json

from types import SimpleNamespace
import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
from databaseManager import databaseManager

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def jsonParse(dict):
   str = dict
   res = Struct(**str)
   return res

@app.route("/")
@swag_from('./databases.yml')
def databases():
    dbs = databaseManager.getDatabases()
    return jsonpickle.encode(dbs)

@app.route('/<id>/')
@swag_from('./database.yml')
def get_db(id):
    db = databaseManager.getDatabase(id)
    return jsonpickle.encode(db)

@app.route('/', methods=['POST'])
@swag_from('./postDatabase.yml')
def post_db():
    name = request.args.get('name')
    databaseManager.addDatabase(name)
    return '', 200

@app.route('/<name>/', methods=['DELETE'])
@swag_from('./deleteDatabase.yml')
def delete_db(name):
    databaseManager.deleteDatabase(name)
    return '', 200

@app.route('/save/<name>/', methods=['PUT'])
@swag_from('./saveDatabase.yml')
def save_db(name):
    databaseManager.save(name)
    return '', 200

@app.route('/open/<name>/', methods=['GET'])
@swag_from('./openDatabase.yml')
def open_db(name):
    db = databaseManager.open(name)
    return jsonpickle.encode(db), 200


@app.route('/<db>/tables/')
@swag_from('./getTables.yml')
def get_tables(db):
    res = databaseManager.getTables(db)
    return jsonpickle.encode(res), 200

@app.route('/<db>/tables/<tb>/')
@swag_from('./getTable.yml')
def get_table(db,tb):
    res = databaseManager.getTable(db,tb)
    print(res)
    return jsonpickle.encode(res), 200

@app.route('/<db>/tables/', methods=['POST'])
@swag_from('./postTable.yml')
def post_table(db):
    table = jsonParse(request.get_json())
    tb = databaseManager.postTable(db,table)

    return jsonpickle.encode(tb), 200

@app.route('/<db>/<tb>/', methods=['DELETE'])
@swag_from('./deleteTable.yml')
def delete_tb(db , tb):
    databaseManager.deleteTable(db,tb)
    return '', 200

@app.route('/<db>/intersect/<tb1>/<tb2>/', methods=['POST'])
@swag_from('./intersect.yml')
def intersect_tb(db , tb1, tb2):
    tb = databaseManager.intersectTables(db,tb1,tb2)
    return jsonpickle.encode(tb), 200


@app.route('/<db>/update/<tb>/', methods=['PUT'])
@swag_from('./updateTable.yml')
def update_rows(db,tb):
    rows = request.get_json()
    res = databaseManager.updateRows(db,tb,rows)

    return jsonpickle.encode(res), 200


app.run(debug=True)
