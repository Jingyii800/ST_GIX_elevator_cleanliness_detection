import json
import logging
import azure.functions as func
import os
import pyodbc

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name(name="historical_data_analysis")
@app.route(route="historical_data_analysis")
def historical_data_analysis(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    conn_str = os.getenv('SqlConnectionString')
    
    try:
        # Connect to the database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        query = "SELECT logID, station, FORMAT(timeStamp, 'yyyy-MM-dd HH:mm:ss') AS created_at FROM Elevator_Cleanliness_Logs;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        result = []
        for row in rows:
            result.append(dict(zip([column[0] for column in cursor.description], row)))

        return func.HttpResponse(json.dumps(result), mimetype="application/json")

    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        return func.HttpResponse("Error connecting to database.", status_code=500)
