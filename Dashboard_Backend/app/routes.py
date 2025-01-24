from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from .database import get_db_connection

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
                SELECT logID, station, elevatorNumber, timeStamp, issue, humidity, infrared, airQuality, passengerReport 
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
            "infrared": row.infrared,
            "airQuality": row.airQuality,
            "passengerReport": bool(row.passengerReport),
        }

        conn.close()
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
    else:
        return jsonify({"error": "Database connection failed"}), 500
    
# Mark false alert
@bp.route('/alerts/<int:alert_id>/false_alarm', methods=["PUT"])
def mark_false_alarm(alert_id):
    """Mark the alert as a false alarm."""

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    

    cursor = conn.cursor()
    query = """
            UPDATE Elevator_Cleanliness_Logs 
            SET falseAlert = 1, confirmed = 1
            WHERE logID = ?
            """
    cursor.execute(query, (alert_id))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Alert {alert_id} issue marked as false alarm."}), 200

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
    conn.close()

    return jsonify({"message": f"Alert {alert_id} confirmed."}), 200

# Display Report Logs
@bp.route('/report_logs', methods=['GET'])
def get_report_logs():
    """Retrieve confirmed reports that are not false alerts with filtering options."""
    # Get query parameters
    time_filter = request.args.get('time_filter', 'daily')  # daily, weekly, monthly, yearly
    station = request.args.get('station', None)
    elevator_num = int(request.args.get('elevator_num', None))

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

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Current Elevator sensor data
@bp.route('/elevator_status', methods=['GET'])
def get_elevator_status():
    """
    Retrieve the latest sensor data for elevators, 
    optionally filtered by station and elevator number.
    """
    station = request.args.get('station', default=None, type=str)
    elevator_num = request.args.get('elevator_num', default=None, type=int)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Base SQL query to get the latest data for each elevator
    query = """
        SELECT Station, Elevator_Num, Humidity, Infrared, AirQuality, PassengerButton, Time
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
        conditions.append("Station = ?")
        params.append(station)

    if elevator_num is not None:
        conditions.append("Elevator_Num = ?")
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
            "infrared": row.Infrared,
            "air_quality": row.AirQuality,
            "passenger_button": bool(row.PassengerButton),
        })

    return jsonify(sensor_data), 200