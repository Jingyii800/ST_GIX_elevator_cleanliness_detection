from azure.iot.device import IoTHubDeviceClient, Message
import json

# Replace with your IoT device connection string from IoT Hub (NOT Event Hub)
DEVICE_CONNECTION_STRING = ""

def send_test_message():
    """Send a test message to IoT Hub (which will route it to Event Hub and trigger Azure Function)."""
    try:
        # Create an IoT Hub device client
        client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)

        # Sample test message (simulating an IoT device sending sensor data)
        test_event = {
            "station": "University of Washington",
            "elevator_num": 1,
            "sensor": {
                "humidity": 35,
                "airQuality": 190,
                "button": 1
            }
        }

        # Convert to JSON and send
        message = Message(json.dumps(test_event))
        client.send_message(message)

        print("✅ Test message sent to IoT Hub!")
        client.disconnect()

    except Exception as e:
        print(f"❌ Error sending test message: {e}")

if __name__ == "__main__":
    send_test_message()
