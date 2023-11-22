from databaseManager import databaseManager
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, jsonify, request

from mutations import *
from queries import *

type_defs = load_schema_from_path("schema.graphql")

query = ObjectType("Query")
mutation = ObjectType("Mutation")

mutation.set_field("createDatabase", create_database_resolver)
mutation.set_field("importDatabase", import_database_resolver)
mutation.set_field("createTable", create_table_resolver)
mutation.set_field("updateRows", update_table_resolver)
mutation.set_field("intersectTables", intersect_tables_resolver)

query.set_field("databases", get_databases_resolver)
query.set_field("tables", get_tables_resolver)
query.set_field("database", get_database_resolver)
query.set_field("table", get_table_resolver)

schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

app = Flask(__name__)

explorer_html = ExplorerGraphiQL().html(None)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return explorer_html , 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)