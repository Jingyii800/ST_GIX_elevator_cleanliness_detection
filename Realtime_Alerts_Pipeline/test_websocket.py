import requests

WEBSOCKET_SERVER_URL = "https://fastapi-websocket-app-fdh0bnc8ffgtdecu.westus-01.azurewebsites.net/send_alert"
def send_alert(station, elevator_num, issue):
    """Send an alert message to the WebSocket server."""
    headers = {"Content-Type": "application/json"}  # ✅ Explicitly set JSON headers
    message = {
        "station": station,
        "elevator_num": elevator_num,
        "issue": issue
    }

    response = requests.post(WEBSOCKET_SERVER_URL, json=message, headers=headers)
    
    if response.status_code == 200:
        print("✅ Alert sent to WebSocket server successfully!")
        print(response.json())
    else:
        print(f"❌ Failed to send alert: {response.status_code} - {response.text}")

if __name__ == "__main__":
    send_alert("University of Washington", 1, "Liquid")