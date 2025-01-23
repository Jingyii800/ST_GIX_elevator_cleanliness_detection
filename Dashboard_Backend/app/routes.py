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
        cursor.execute("SELECT logID, station, issue, timeStamp FROM Elevator_Cleanliness_Logs WHERE resolved = 0")
        alerts = cursor.fetchall()
        conn.close()

        alert_list = []
        for row in alerts:
            alert_list.append({
                'logID': row.logID,
                'station': row.station,
                'issue': row.issue,
                'timeStamp': row.timeStamp.strftime('%Y-%m-%d %H:%M:%S')
            })

        return jsonify(alert_list)
    else:
        return jsonify({"error": "Database connection failed"}), 500