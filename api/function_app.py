import azure.functions as func
import logging
import json

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