import Adafruit_DHT

# Set the sensor type (DHT22)
SENSOR = Adafruit_DHT.DHT22

# Set the GPIO pin where the data pin is connected
GPIO_PIN = 4  # Change this if you're using a different GPIO pin

print("Reading data from DHT22 sensor...")

try:
    while True:
        # Read the temperature and humidity
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO_PIN)

        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%")
        else:
            print("Failed to retrieve data from the sensor. Retrying...")

except KeyboardInterrupt:
    print("\nProgram stopped.")
