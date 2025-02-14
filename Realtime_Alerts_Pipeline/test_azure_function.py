from azure.eventhub import EventHubProducerClient, EventData
import json

# Replace with your actual Event Hub details
EVENT_HUB_CONNECTION_STRING = ""
EVENT_HUB_NAME = "elevator_clean"

def send_test_message():
    """Send a test event to Azure Event Hub to trigger the Azure Function."""
    try:
        # Create Event Hub producer client
        producer = EventHubProducerClient.from_connection_string(EVENT_HUB_CONNECTION_STRING, eventhub_name=EVENT_HUB_NAME)

        # Create test event data
        test_event = {
            "station": "Downtown",
            "elevator_num": 3,
            "sensor": {
                "humidity": 25,
                "airQuality": 180,
                "button": 1
            }
        }

        # Convert to JSON and add to batch
        event_data_batch = producer.create_batch()
        event_data_batch.add(EventData(json.dumps(test_event)))

        # Send the batch
        producer.send_batch(event_data_batch)
        print("✅ Test message sent successfully!")

    except Exception as e:
        print(f"❌ Error sending test message: {e}")

    finally:
        producer.close()

if __name__ == "__main__":
    send_test_message()
