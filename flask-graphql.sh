#!/bin/sh
export FLASK_APP=graphql-app.py
python -m pipenv run flask --debug run -h 0.0.0.0
$SHELL