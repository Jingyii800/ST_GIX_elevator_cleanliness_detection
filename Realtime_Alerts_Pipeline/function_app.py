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
import requests

app = func.FunctionApp()
conn_str = os.getenv('SqlConnectionString')

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="elevatorcleanlinessdetect",
                               connection="EventHubConnectionString") 

def eventhub_trigger(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
    
    # Decode the message and convert from JSON
    message_body = azeventhub.get_body().decode('utf-8')
    data = json.loads(message_body)
    print(data)
    
    try:
        # Connect to the database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        station = data.get("station")
        elevator_num = data.get("elevator_num")

        check_alert_query = """
            SELECT COUNT(*) FROM Elevator_Sensor_Status 
            WHERE Station = ? AND Elevator_Num = ? AND Alert_Status = 'Active'
            """
        cursor.execute(check_alert_query, (station, elevator_num))
        active_alert_count = cursor.fetchone()[0]

        if active_alert_count > 0:
            logging.info(f"🚨 Active alert already exists for {station}, Elevator {elevator_num}. Skipping redundant alert log.")
        else:
            # Process sensor data
            humidity = data["sensor"]["humidity"]
            air_quality = data["sensor"]["airQuality"]
            passenger_button = data["sensor"]["button"]
            timestamp = datetime.utcnow()            

            # TODO: Optinal :check abnormal_counts based on Machine Learning from database
            
            # 🟢 Define Status Based on Thresholds
            humidity_status = "Warning" if humidity > 32.5 else "Good"
            air_quality_status = "Warning" if air_quality > 150 else "Good"
            passenger_button_status = "Warning" if passenger_button == 1 else "Good"

            # 🟡 Count Warnings (if 2+ AND air quality is bad, trigger an alert)
            warning_count = sum([humidity_status == "Warning", passenger_button_status == "Warning"])

            # 📝 Insert Sensor Data into Elevator_Sensor_Status
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Round values before inserting into the table
            humidity = round(humidity, 1)
            air_quality = round(air_quality, 1)

            # 🚨 Insert Alert if Conditions Met
            if air_quality_status == "Warning" and warning_count >= 1:
                alert_status = "Active"

                # ✅ Insert New Alert in Logs
                alert_query = """
                    INSERT INTO Elevator_Cleanliness_Logs 
                    (timeStamp, station, elevatorNumber, Issue, Humidity, AirQuality, PassengerReport)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(alert_query, (timestamp, station, elevator_num, "Liquid", humidity, air_quality, passenger_button))

                send_alert(station, elevator_num, "Liquid")
                # ✅ Trigger WebSocket Alert
                logging.info(f"🚨 Alert Triggered: {station}, Elevator {elevator_num} (Sensor Abnormality)")

            else:
                alert_status = "Normal"

            # 🔄 Upsert Sensor Data (Ensures One Row Per Elevator)
            sensor_query = """
                MERGE INTO Elevator_Sensor_Status AS Target
                USING (SELECT ? AS Station, ? AS Elevator_Num) AS Source
                ON Target.Station = Source.Station AND Target.Elevator_Num = Source.Elevator_Num
                WHEN MATCHED THEN 
                    UPDATE SET 
                        Time = ?, Humidity = ?, Humidity_Status = ?, 
                        AirQuality = ?, AirQuality_Status = ?, 
                        PassengerButton = ?, PassengerButton_Status = ?, 
                        Alert_Status = ?
                WHEN NOT MATCHED THEN 
                    INSERT (Time, Station, Elevator_Num, Humidity, Humidity_Status, 
                                AirQuality, AirQuality_Status, 
                            PassengerButton, PassengerButton_Status, Alert_Status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(sensor_query, 
                (station, elevator_num, timestamp, humidity, humidity_status, 
                air_quality, air_quality_status, 
                passenger_button, passenger_button_status, alert_status, 
                timestamp, station, elevator_num, humidity, humidity_status, 
                air_quality, air_quality_status, 
                passenger_button, passenger_button_status, alert_status)
            )

            conn.commit()

    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        return func.HttpResponse("Database error occurred.", status_code=500)
    finally:
        cursor.close()
        conn.close()



def send_alert(station, elevator_num, issue):
    """Send an alert message to the WebSocket server."""
    headers = {"Content-Type": "application/json"}  # ✅ Explicitly set JSON headers
    message = {
        "station": station,
        "elevator_num": elevator_num,
        "issue": issue
    }
    WEBSOCKET_SERVER_URL = "https://fastapi-websocket-app-fdh0bnc8ffgtdecu.westus-01.azurewebsites.net/send_alert"
    response = requests.post(WEBSOCKET_SERVER_URL, json=message, headers=headers)
    
    if response.status_code == 200:
        print("✅ Alert sent to WebSocket server successfully!")
        print(response.json())
    else:
        print(f"❌ Failed to send alert: {response.status_code} - {response.text}")


