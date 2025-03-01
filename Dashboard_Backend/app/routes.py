from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, url_for

from app.send_emails import send_email
from .database import get_db_connection
from flask import render_template_string
import os

bp = Blueprint('main', __name__)

# Get all alerts
# 0 -> False 1 -> True
@bp.route('/alerts', methods=['GET'])
def get_alerts():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = """
                SELECT logID, station, elevatorNumber 
                FROM Elevator_Cleanliness_Logs 
                WHERE confirmed = 0
                """
        cursor.execute(query)
        alerts = cursor.fetchall()
        conn.close()

        alert_list = []
        for row in alerts:
            alert_list.append({
                'logID': row.logID,
                'station': row.station,
                'elevatorNumber': row.elevatorNumber,
            })

        print(alert_list)
        return jsonify(alert_list)
    else:
        return jsonify({"error": "Database connection failed"}), 500
    
# Get specific alert
@bp.route('/alerts/<int:alert_id>', methods=["GET"])
def get_alerts_by_id(alert_id):
    """Fetch a specific alert by ID."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = """
                SELECT logID, station, elevatorNumber, timeStamp, issue, humidity, airQuality, passengerReport 
                FROM Elevator_Cleanliness_Logs
                WHERE logID = ?
                """
        cursor.execute(query, (alert_id))
        row = cursor.fetchone()

        if not row:
            return jsonify({'error':"Alert Not Found"}), 404
        
        alert_detail = {
            "id": row.logID,
            "station": row.station,
            "elevatorNum": row.elevatorNumber,
            "time": row.timeStamp,
            "issue": row.issue,
            "humidity": row.humidity,
            "airQuality": row.airQuality,
            "passengerReport": bool(row.passengerReport),
        }

        conn.close()
        print(alert_detail)
        return jsonify(alert_detail)
    
#Update Alert issue
@bp.route('/alerts/<int:alert_id>/update_issue', methods=["PUT"])
def update_alerts(alert_id):
    """Update the issue type of an alert (solid/liquid)."""
    data = request.get_json()
    new_issue = data.get("issue")

    if new_issue not in ["solid", "liquid"]:
        return jsonify({'error': 'Invalid Issue Type'}), 400  # Fixed JSON format
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = """
                UPDATE Elevator_Cleanliness_Logs 
                SET issue = ? 
                WHERE logID = ?
                """
        cursor.execute(query, (new_issue, alert_id))
        conn.commit()
        conn.close()

        return jsonify({"message": f"Alert {alert_id} issue updated to {new_issue}."}), 200
        print("success")
    else:
        return jsonify({"error": "Database connection failed"}), 500
    
# Mark false alert
@bp.route('/alerts/<int:alert_id>/false_alarm', methods=["PUT"])
def mark_false_alarm(alert_id):
    """Mark the alert as a false alarm and reset elevator alert status."""

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()

        # 🔹 Fetch station & elevator number related to the alert
        query_fetch = """
            SELECT station, elevatorNumber 
            FROM Elevator_Cleanliness_Logs 
            WHERE logID = ?
        """
        cursor.execute(query_fetch, (alert_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": f"Alert {alert_id} not found."}), 404

        station, elevator_num = result

        # ✅ Mark False Alert in Logs
        query_update_log = """
            UPDATE Elevator_Cleanliness_Logs 
            SET falseAlert = 1, confirmed = 1, resolved = 1
            WHERE logID = ?
        """
        cursor.execute(query_update_log, (alert_id,))

        # ✅ Update Alert Status in `Elevator_Sensor_Status`
        query_update_sensor = """
            UPDATE Elevator_Sensor_Status 
            SET Alert_Status = 'Normal'
            WHERE Station = ? AND Elevator_Num = ?
        """
        cursor.execute(query_update_sensor, (station, elevator_num))

        conn.commit()

        return jsonify({"message": f"Alert {alert_id} marked as false alarm. Elevator {elevator_num} status reset to 'Normal'."}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# Confirm alert and notify staff
@bp.route('/alerts/<int:alert_id>/confirm_alert', methods=['PUT'])
def confirm_alert(alert_id):
    """Mark the alert as confirmed and notify staff."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    query = "UPDATE Elevator_Cleanliness_Logs SET confirmed = 1 WHERE logID = ?"
    cursor.execute(query, (alert_id,))
    conn.commit()

    # Fetch elevator details
    cursor.execute("SELECT station, elevatorNumber FROM Elevator_Cleanliness_Logs WHERE logID = ?", (alert_id,))
    alert_data = cursor.fetchone()
    conn.close()

    if not alert_data:
        return jsonify({"error": "No valid alert found"}), 500

    station, elevator_num = alert_data

    # Fixed test email address
    test_email = "jingyj11@uw.edu"

    # Generate button link
    confirm_cleaning_url = request.url_root + url_for('main.confirm_cleaning', alert_id=alert_id)

    # Load HTML template
    template_path = os.path.join(os.path.dirname(__file__), 'templates/email_alerts_template.html')
    with open(template_path, 'r') as f:
        email_template = f.read()

    # Render email with dynamic values
    email_content = render_template_string(
        email_template,
        station=station,
        elevator_num=elevator_num,
        confirm_cleaning_url=confirm_cleaning_url
    )

    # Send email (fixed test email)
    send_email(test_email, "Elevator Cleanliness Alert - Test", email_content)

    return jsonify({"message": "Alert confirmed and test email sent"}), 200

# Display Report Logs
@bp.route('/report_logs', methods=['GET'])
def get_report_logs():
    """Retrieve confirmed reports that are not false alerts with filtering options."""
    # Get query parameters
    time_filter = request.args.get('time_filter', 'daily')  # daily, weekly, monthly, yearly
    station = request.args.get('station', None)
    elevator_num_str = request.args.get('elevator_num', None)
    elevator_num = int(elevator_num_str) if elevator_num_str else None
    print(time_filter, station, elevator_num)

    # Date filter logic
    now = datetime.now()
    if time_filter == 'daily':
        start_date = now - timedelta(days=1)
    elif time_filter == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif time_filter == 'monthly':
        start_date = now - timedelta(days=30)
    elif time_filter == 'yearly':
        start_date = now - timedelta(days=1000)
    else:
        return jsonify({"error": "Invalid time filter"}), 400

    # SQL query with filtering
    query = """
        SELECT station, elevatorNumber, timeStamp, resolved, duration, resolvedBy
        FROM Elevator_Cleanliness_Logs
        WHERE confirmed = 1 AND falseAlert = 0
          AND timeStamp >= ?
    """
    formatted_data = start_date.strftime('%Y-%m-%d %H:%M:%S')
    params = [formatted_data]

    if station:
        query += " AND station = ?"
        params.append(station)
    
    if elevator_num:
        query += " AND elevatorNumber = ?"
        params.append(elevator_num)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        print(query, params)
        cursor.execute(query, params)
        logs = cursor.fetchall()
        conn.close()

        # Format results
        results = [
            {
                "station": row.station,
                "elevatorNumber": row.elevatorNumber,
                "timeStamp": row.timeStamp.strftime("%Y-%m-%d %H:%M:%S"),
                "resolved": bool(row.resolved),
                "resolvedBy": row.resolvedBy,
                "duration": row.duration,
            }
            for row in logs
        ]
        print(results)
        return jsonify(results), 200


    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Current Elevator sensor data
@bp.route('/elevator_status', methods=['GET'])
def get_elevator_status():
    """
    Retrieve the latest sensor data and status for elevators, 
    optionally filtered by station and elevator number.
    """
    station = request.args.get('station', default=None, type=str)
    elevator_num = request.args.get('elevator_num', default=None, type=int)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Updated SQL query to retrieve both sensor values and their corresponding status
    query = """
        SELECT 
            ESS.Station, 
            ESS.Elevator_Num, 
            ESS.Humidity, 
            ESS.Humidity_Status,
            ESS.AirQuality, 
            ESS.AirQuality_Status,
            ESS.PassengerButton,
            ESS.PassengerButton_Status,
            ESS.Alert_Status,  -- ✅ Added Alert Status
            ESS.Time
        FROM Elevator_Sensor_Status AS ESS
        WHERE Time = (
            SELECT MAX(Time)
            FROM Elevator_Sensor_Status
            WHERE Station = ESS.Station AND Elevator_Num = ESS.Elevator_Num
        )
    """

    # Add filters for station and elevator number if provided
    conditions = []
    params = []

    if station:
        conditions.append("ESS.Station = ?")
        params.append(station)

    if elevator_num is not None:
        conditions.append("ESS.Elevator_Num = ?")
        params.append(elevator_num)

    # If filters exist, append them to the query
    if conditions:
        query += " AND " + " AND ".join(conditions)

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()

    # Formatting results into a list of dictionaries
    sensor_data = []
    for row in results:
        sensor_data.append({
            "station": row.Station,
            "elevator_num": row.Elevator_Num,
            "humidity": row.Humidity,
            "humidity_status": row.Humidity_Status,
            "air_quality": row.AirQuality,
            "air_quality_status": row.AirQuality_Status,
            "passenger_button": bool(row.PassengerButton),
            "passenger_button_status": row.PassengerButton_Status,
            "alert_status": row.Alert_Status,  # ✅ Added Alert Status
            "time": row.Time
        })

    return jsonify(sensor_data), 200

from flask import request
import logging
from datetime import datetime

@bp.route('/alerts/<int:alert_id>/confirm_cleaning', methods=['PUT'])
def confirm_cleaning(alert_id):
    """Endpoint for staff to mark cleaning as completed based on alert_id."""
    data = request.get_json()
    staff = data.get("staff", "Unknown")

    try:
        resolved_time = datetime.strptime(data.get("resolved_time"), "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()

    # Get station and elevator number using alert_id
    query = """
        SELECT station, elevatorNumber, timeStamp 
        FROM Elevator_Cleanliness_Logs 
        WHERE logID = ? AND confirmed = 1 AND resolved = 0
    """
    cursor.execute(query, (alert_id,))
    alert_data = cursor.fetchone()

    if not alert_data:
        logging.warning(f"No unresolved report found for alert ID {alert_id}")
        return jsonify({"error": f"No unresolved report found for alert ID {alert_id}"}), 404

    station, elevator_num, reported_time = alert_data

    # Calculate duration in minutes
    duration = (resolved_time - reported_time).total_seconds() // 60

    # Update Elevator_Cleanliness_Logs database
    update_query = """
        UPDATE Elevator_Cleanliness_Logs 
        SET resolved = 1, resolvedBy = ?, resolvedTime = ?, duration = ? 
        WHERE logID = ?
    """
    cursor.execute(update_query, (staff, resolved_time, duration, alert_id))

    # Update Elevator_Sensor_Status to 'Normal'
    sensor_status_query = """
        UPDATE Elevator_Sensor_Status
        SET Alert_Status = 'Normal'
        WHERE Station = ? AND Elevator_Num = ?
    """
    cursor.execute(sensor_status_query, (station, elevator_num))

    conn.commit()
    conn.close()

    logging.info(f"✅ Issue resolved for {station}, Elevator {elevator_num} by {staff} (Duration: {duration} min)")

    return jsonify({"message": "Cleaning marked as completed", "alert_id": alert_id, "station": station, "elevator_num": elevator_num, "duration": duration}), 200
