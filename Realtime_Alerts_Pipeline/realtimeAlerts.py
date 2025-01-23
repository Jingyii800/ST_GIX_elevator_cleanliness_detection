# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

import json
import logging
import azure.functions as func
import os
import pyodbc

blueprint = func.Blueprint()
conn_str = os.getenv('SqlConnectionString')

@blueprint.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="myeventhub",
                               connection="EventHubConnectionString") 
def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
    
    # Decode the message and convert from JSON
    message_body = azeventhub.get_body().decode('utf-8')
    data = json.loads(message_body)

    # Connect to the database
    # conn = pyodbc.connect(conn_str)
    # cursor = conn.cursor()

    # query = "SELECT logID, station, FORMAT(timeStamp, 'yyyy-MM-dd HH:mm:ss') AS created_at FROM Elevator_Cleanliness_Logs;"
    # cursor.execute(query)
    # rows = cursor.fetchall()
    # conn.close()

    # sensor:
        # humidity sensor
        # infrared sensor
        # air quality sensor
        # button
    # nfc
    # time
    # location

    # if "sensor" not in data:
        # process nfc
        # update in SQL Logs database: marked as True, staff: John, Resolved Time:xxx, Duration, count

    # else:
        # if detect abnormal >= 3
            # write in SQL database
            # Primary Key(autoincremented) | Time | Location | Comfirmed | FalseAlert | Issue | Resolved | Resolved_Staff| Resolve Time | Duration | Humidity | Infrared | Air Quality | Passenger_Reported
            #     int                        str      str       boolean     boolean     str     boolean      str             str           int       float        float    float             boolean
            # trigger alert (WebSocket)



