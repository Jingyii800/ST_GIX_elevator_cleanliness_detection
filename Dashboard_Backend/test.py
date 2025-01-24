import requests

# Base URL of your Flask app
BASE_URL = "http://127.0.0.1:5000"

# # Test: Get all active alerts
# response = requests.get(f"{BASE_URL}/alerts")
# print("Get Active Alerts:", response.status_code, response.json())

# # Test: Get a specific alert by ID
# alert_id = 5
# response = requests.get(f"{BASE_URL}/alerts/{alert_id}")
# print("Get Alert Details:", response.status_code, response.json())

# # Test: Update issue type to "liquid"
# update_payload = {"issue": "liquid"}
# response = requests.put(f"{BASE_URL}/alerts/{alert_id}/update_issue", json=update_payload)
# print("Update Issue:", response.status_code, response.json())

# # Test: Mark alert as false alarm
# response = requests.put(f"{BASE_URL}/alerts/{alert_id}/false_alarm")
# print("Mark False Alarm:", response.status_code, response.json())

# # Test: Confirm alert and notify staff
# response = requests.put(f"{BASE_URL}/alerts/{alert_id}/confirm_alert")
# print("Confirm Alert:", response.status_code, response.json())

# Test get reports logs
response = requests.get(f"{BASE_URL}/report_logs?time_filter=yearly&station=Beacon Hill&elevator_num=2")
print("Get Report", response.status_code, response.json())