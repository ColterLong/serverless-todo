import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="getData")
def getData(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    value = req.params.get('value')
    if not value:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            value = req_body.get('value')

    if value == 'list':
        return func.HttpResponse(json.dumps([
            {
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
        ]))
    elif value == 'name':
        return func.HttpResponse(
             "Colt",
             status_code=200
        )
    else:
        return func.HttpResponse(
             "Name",
             status_code=200
        )
    
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
    return func.HttpResponse(
             "post response",
             status_code=200
        )