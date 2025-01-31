# Register this blueprint by adding the following line of code 
# to your entry point file.  
# app.register_functions(blueprint) 
# 
# Please refer to https://aka.ms/azure-functions-python-blueprints

from datetime import datetime
import json
import logging
import azure.functions as func
import os
import pyodbc

app = func.FunctionApp()
conn_str = os.getenv('SqlConnectionString')

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="myeventhub",
                               connection="EventHubConnectionString") 

def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
    
    # Decode the message and convert from JSON
    message_body = azeventhub.get_body().decode('utf-8')
    data = json.loads(message_body)
    
    try:
        # Connect to the database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # sensor:
            # humidity
            # infrared
            # airQuality
            # button
        # nfc
        # time
        station = data.get("station")
        elevator_num = data.get("elevator_num")

        if "sensor" not in data:
            # Process NFC event (staff intervention)
            staff = data.get("staff", "Unknown")
            resolved_time = datetime.strptime(data.get("resolved_time"), "%Y-%m-%dT%H:%M:%S")

            # Get the most recent unresolved report for this station
            query = """
            SELECT logID, timeStamp 
            FROM Elevator_Cleanliness_Logs 
            WHERE confirmed = 1 AND station = ? AND elevatorNumber = ? AND resolved = 0 
            ORDER BY timeStamp DESC
            """
            cursor.execute(query, station, elevator_num)
            reported_time_row = cursor.fetchone()
            
            if reported_time_row:
                logID, reported_time = reported_time_row
                duration = (resolved_time - reported_time).total_seconds() // 60  # Convert to minutes
            else:
                logging.warning(f"No unresolved reports found for station {station}")
                return func.HttpResponse(f"No unresolved reports found for station {station}", status_code=404)

            # update in SQL Logs database: marked as True, staff: John, Resolved Time:xxx, Duration
            update_query = """
            UPDATE Elevator_Cleanliness_Logs 
            SET resolved = 1, resolvedBy = ?, resolveTime = ?, duration = ? 
            WHERE logID = ?
            """
            cursor.execute(update_query, staff, resolved_time, duration, logID)
            logging.info(f"NFC data processed and issue resolved for station {station} by {staff}. Duration: {duration} minutes.")

        else:
            # Process sensor data
            humidity = data["sensor"]["humidity"]
            infrared = data["sensor"]["infrared"]
            air_quality = data["sensor"]["airQuality"]
            passenger_button = data["sensor"]["button"]
            timestamp = datetime.utcnow()            
            # write current data in table Elevator_Sensor_Status
            # Insert into Elevator_Sensor_Status table
            sensor_insert_query = """
            INSERT INTO Elevator_Sensor_Status (Time, Station, Elevator_Num, Humidity, Infrared, AirQuality, PassengerButton)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sensor_insert_query, timestamp, station, elevator_num, humidity, infrared, air_quality, passenger_button)
            logging.info("Sensor data stored successfully.")

            # TODO: check abnormal_counts based on Machine Learning from database
            
            # Check for abnormal sensor values
            air_quality_abnormal = air_quality < 50  # Threshold for air quality
            humidity_abnormal = humidity > 80  # Threshold for humidity
            infrared_abnormal = infrared > 30  # Threshold for infrared
            button_abnormal = passenger_button == 1  # Button pressed

            abnormal_count = sum([humidity_abnormal, infrared_abnormal, button_abnormal])

            if air_quality_abnormal and abnormal_count >= 2:
                # Log abnormality in Elevator_Cleanliness_Logs
                alert_query = """
                INSERT INTO Elevator_Cleanliness_Logs (timeStamp, station, elevatorNumber, Issue, Humidity, Infrared, Air_Quality, Passenger_Reported)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(alert_query, timestamp, station, elevator_num, "liquid", humidity, infrared, air_quality, passenger_button)

                # Trigger an alert via WebSocket (pseudo function call)
                send_alert(station, elevator_num, "Sensor Abnormality detected")
                logging.info(f"Alert triggered for Station: {station}, Elevator: {elevator_num}")

        conn.commit()

    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        return func.HttpResponse("Database error occurred.", status_code=500)
    finally:
        cursor.close()
        conn.close()

def send_alert(station, elevator_num, issue):
    pass



