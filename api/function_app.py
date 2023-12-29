import azure.functions as func
import logging
import json

import os
import pyodbc, struct
from azure import identity
from typing import Union
from pydantic import BaseModel

todos = [{
                "category": "personal",
                "content": "test message 1",
                "createdAt": 1703632030060,
                "done": False
            },
            {
                "category": "business",
                "content": "test message 2",
                "createdAt": 1703631889087,
                "done": False
            },
        ]
name = {"name": "enterName"}

# connection_string = 'insert string here'
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="getName")
def getName(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(json.dumps(name))

@app.route(route="getTodos")
def getTodos(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(json.dumps(todos))
    
@app.route(route="addTodo")
def addTodo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a POST request.')

    if req.method.lower() != "post":
        return func.HttpResponse(
             "HTTP request must be POST",
             status_code=405
        )

    logging.info('outputting post data:')
    logging.info(req.get_json())
    todos.append(req.get_json())
    return func.HttpResponse(json.dumps(todos))

@app.route(route="removeTodo")
def removeTodo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a POST request to delete.')
    logging.info('outputting post data:')
    logging.info(req.get_json())
    todos.remove(req.get_json())
    return func.HttpResponse(json.dumps(todos))

@app.route(route="setName")
def setName(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a POST request to set name.')
    logging.info('outputting post data:')
    logging.info(req.get_json())
    name = req.get_json()
    return func.HttpResponse(json.dumps(name))

@app.route(route="makeTable")
def makeTable(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a POST request to set name.')
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE [dbo].[Personss] (
            [id]   INT NOT NULL,
            [name] TEXT NULL,
            CONSTRAINT [PK_Personss] PRIMARY KEY CLUSTERED ([id] ASC)
        );""")

        conn.commit()
        return func.HttpResponse("Made new table")
    except Exception as e:
        # Table may already exist
        logging.info("error, table may already exist")
        logging.info(e)
        return func.HttpResponse("Table already exists")
    
@app.route(route="pullTable")
def pullTable(req: func.HttpRequest) -> func.HttpResponse:
    rows = []
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM [dbo].[Personss]")
    
        all = cursor.fetchall()
        logging.info(all)
        allDict = {"id": all[0].id,
                   "name": all[0].name}
        logging.info(allDict)
    return func.HttpResponse(json.dumps(allDict))