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
    print(data)
    
    try:
        # Connect to the database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # sensor:
            # humidity
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

            cursor.execute("""
            UPDATE Elevator_Sensor_Status
            SET Alert_Status = 'Normal
            WHERE Station = ? AND Elevator_Num = ?""", station, elevator_num)
            logging.info(f"✅ Issue resolved for {station}, Elevator {elevator_num} by {staff} (Duration: {duration} min)")

        else:
            # Process sensor data
            humidity = data["sensor"]["humidity"]
            air_quality = data["sensor"]["airQuality"]
            passenger_button = data["sensor"]["button"]
            timestamp = datetime.utcnow()            

            # TODO: Optinal :check abnormal_counts based on Machine Learning from database
            
            # 🟢 Define Status Based on Thresholds
            humidity_status = "Warning" if humidity > 80 else "Good"
            air_quality_status = "Warning" if air_quality > 2 else "Good"
            passenger_button_status = "Warning" if passenger_button == 1 else "Good"

            # 🟡 Count Warnings (if 2+ AND air quality is bad, trigger an alert)
            warning_count = sum([humidity_status == "Warning", passenger_button_status == "Warning"])

            # 📝 Insert Sensor Data into Elevator_Sensor_Status
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 🚨 Insert Alert if Conditions Met
            if air_quality_status == "Warning" and warning_count >= 2:
                alert_status = "Active"

                # ✅ Insert New Alert in Logs
                alert_query = """
                    INSERT INTO Elevator_Cleanliness_Logs 
                    (timeStamp, station, elevatorNumber, Issue, Humidity, AirQuality, PassengerReport, confirmed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
                """
                cursor.execute(alert_query, (timestamp, station, elevator_num, "Liquid", humidity, air_quality, passenger_button))

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
                            Infrared, Infrared_Status, AirQuality, AirQuality_Status, 
                            PassengerButton, PassengerButton_Status, Alert_Status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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
    pass



