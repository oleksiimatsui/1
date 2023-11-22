


from flask import Flask
import requests

url = "http://127.0.0.1:5000"

def setup_and_intersect():
    requests.post(url + "?name=1")
    requests.post(url + "/1/tables", json={
        "id": 0,
        "name": "Table_1",
        "fields": [
            {"name": "A", "type": "Int"},
            {"name": "B", "type": "Int"}
        ]
    })
    requests.post(url + "/1/tables", json={
        "id": 0,
        "name": "Table_2",
        "fields": [
            {"name": "A", "type": "Int"},
            {"name": "B", "type": "Int"}
        ]
    })
    requests.put(url + "/1/update/1", json=[
        {
            "A": "1",
            "B": "2"
        },
        {
            "A": "2",
            "B": "2"
        },
        {
            "A": "1",
            "B": "3"
        }
    ])
    requests.put(url + "/1/update/2", json=[
        {
            "A": "1",
            "B": "2"
        },
        {
            "A": "2",
            "B": "2"
        },
        {
            "A": "3",
            "B": "3"
        }
    ])
    requests.post(url + "/1/intersect/1/2")
    print(requests.get(url + "/1/tables/3").content)


setup_and_intersect()