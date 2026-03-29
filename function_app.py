import azure.functions as func
import logging
import os
from azure.data.tables import TableServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitorcounter")
def visitorcounter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Visitor counter function processed a request. - v2')

    connection_string = os.environ["COSMOS_CONNECTION_STRING"]
    table_name = "visitorcounter"

    table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = table_service.get_table_client(table_name=table_name)

    try:
        entity = table_client.get_entity(partition_key="counter", row_key="visits")
        count = entity["count"]
        count += 1
        entity["count"] = count
        table_client.update_entity(entity)
    except Exception:
        count = 1
        table_client.upsert_entity({
            "PartitionKey": "counter",
            "RowKey": "visits",
            "count": count
        })

    return func.HttpResponse(
        f'{{"count": {count}}}',
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"},
        status_code=200
    )