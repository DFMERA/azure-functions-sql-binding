import logging
import json

import azure.functions as func


def main(req: func.HttpRequest, todoItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass

    if req_body:
        sql_rows = func.SqlRowList(map(lambda r: func.SqlRow.from_dict(r), req_body))
        todoItems.set(sql_rows)
        
        logging.info(json.dumps(req_body))
        return func.HttpResponse(
            body=json.dumps(req_body),
            status_code=201,
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
            "Error accessing request body",
            status_code=400
        )
