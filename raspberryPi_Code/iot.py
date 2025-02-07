#!/usr/bin/env python3
"""
This script reads data from multiple sensors:
  - MQ2 gas sensor (via ADS1115 on channel A0)
  - DHT22 temperature/humidity sensor (GPIO4)
  - A button (GPIO17)
  - An RFID RC522 module (using SimpleMFRC522)
  
It sends the collected data as JSON messages to Azure IoT Hub.
"""

import os
import time
import json
import logging
import datetime
import threading

import board
import busio
import digitalio

import adafruit_dht
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Import the SimpleMFRC522 library for RC522 RFID (SPI-based)
from mfrc522 import SimpleMFRC522

from azure.iot.device import IoTHubDeviceClient, Message

# ==========================================
# Configuration & Azure IoT Hub Connection
# ==========================================

# ***** Replace the following with your actual connection string *****
IOTHUB_CONNECTION_STRING = "HostName=elevatorCleanlinessDetector.azure-devices.net;DeviceId=ElevatorDetector;SharedAccessKey=lrTZ47/DX3nWRc4kPtILKfqFf22+7+ojF+7L9GpihnY="

# Station/elevator identifiers (adjust as needed)
STATION = "University of Washington"
ELEVATOR_NUM = 1

# ==========================================
# Logging Configuration
# ==========================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IoT_Device")

# ==========================================
# Initialize Azure IoT Hub Device Client
# ==========================================
try:
    device_client = IoTHubDeviceClient.create_from_connection_string(IOTHUB_CONNECTION_STRING)
    device_client.connect()
    logger.info("Connected to Azure IoT Hub.")
except Exception as e:
    logger.error("Failed to connect to Azure IoT Hub: " + str(e))
    exit(1)

# ==========================================
# Initialize Sensors and Input Devices
# ==========================================

# Shared I2C bus for ADS1115 (MQ2 sensor)
try:
    i2c = busio.I2C(board.SCL, board.SDA)
except Exception as e:
    logger.error("Failed to initialize I2C: " + str(e))
    exit(1)

# (1) ADS1115 for MQ2 sensor (air quality)
try:
    ads = ADS.ADS1115(i2c)
    ads.gain = 1
    mq2_channel = AnalogIn(ads, ADS.P0)
    logger.info("ADS1115 (MQ2 sensor) initialized.")
except Exception as e:
    logger.error("Failed to initialize ADS1115: " + str(e))
    exit(1)

# (2) DHT22 sensor on GPIO4
try:
    dht_sensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    logger.info("DHT22 sensor initialized on GPIO4.")
except Exception as e:
    logger.error("Failed to initialize DHT22 sensor: " + str(e))
    exit(1)

# (3) Button on GPIO17 with internal pull-up
try:
    button = digitalio.DigitalInOut(board.D17)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    logger.info("Button initialized on GPIO17.")
except Exception as e:
    logger.error("Failed to initialize button: " + str(e))
    exit(1)

# (4) RFID RC522 module (using SPI via SimpleMFRC522)
# The SimpleMFRC522 library handles SPI initialization internally.
# Create a global reader instance.
try:
    rfid_reader = SimpleMFRC522()
    logger.info("RFID RC522 module initialized.")
except Exception as e:
    logger.error("Failed to initialize RFID RC522 module: " + str(e))
    exit(1)

# ==========================================
# Helper Function to Send Data to Azure IoT Hub
# ==========================================
def send_message_to_iothub(payload_dict):
    try:
        message_json = json.dumps(payload_dict)
        msg = Message(message_json)
        device_client.send_message(msg)
        logger.info("Sent message to Azure IoT Hub: " + message_json)
    except Exception as e:
        logger.error("Error sending message: " + str(e))

# ==========================================
# RFID Reading Thread Function
# ==========================================
def rfid_thread():
    """Continuously wait for an RFID card and send its info to IoT Hub."""
    while True:
        try:
            # The read() method blocks until a card is detected.
            card_id, card_text = rfid_reader.read()
            rfid_payload = {
                "station": STATION,
                "elevator_num": ELEVATOR_NUM,
                "nfc": {
                    "id": card_id,
                    "text": card_text.strip() if card_text else ""
                },
                "time": datetime.datetime.utcnow().isoformat() + "Z"
            }
            send_message_to_iothub(rfid_payload)
            logger.info("RFID tag detected: ID: {} Text: {}".format(card_id, card_text))
            # Delay to prevent reading the same card repeatedly.
            time.sleep(5)
        except Exception as e:
            logger.error("RFID read error: " + str(e))
            time.sleep(1)

# Start the RFID reading thread (daemon=True means it will exit when the main program exits)
rfid_thread_instance = threading.Thread(target=rfid_thread, daemon=True)
rfid_thread_instance.start()

# ==========================================
# Main Loop: Read Sensors and Send Data
# ==========================================
logger.info("Starting main sensor loop. Press Ctrl+C to exit.")

while True:
    try:
        # --- Read DHT22 Sensor (temperature and humidity) ---
        try:
            humidity = dht_sensor.humidity
            temperature_c = dht_sensor.temperature
        except RuntimeError as e:
            # DHT sensors may fail intermittently.
            logger.warning("DHT22 read error: " + str(e))
            humidity = None
            temperature_c = None

        # --- Read MQ2 Sensor (air quality) ---
        try:
            mq2_voltage = mq2_channel.voltage
            # You may convert voltage to a concentration value if desired.
            air_quality = mq2_voltage
        except Exception as e:
            logger.error("MQ2 sensor read error: " + str(e))
            air_quality = None

        # --- Read Button ---
        # (Assuming active-low: pressed = False, so invert the value)
        button_pressed = not button.value
        button_val = 1 if button_pressed else 0

        # --- Prepare Sensor Data Payload ---
        sensor_payload = {
            "station": STATION,
            "elevator_num": ELEVATOR_NUM,
            "sensor": {
                "humidity": humidity if humidity is not None else 0,
                "temperature": temperature_c if temperature_c is not None else 0,
                "airQuality": air_quality if air_quality is not None else 0,
                "button": button_val
            },
            "time": datetime.datetime.utcnow().isoformat() + "Z"
        }

        # Send sensor data to Azure IoT Hub.
        send_message_to_iothub(sensor_payload)

        # Polling interval (adjust as needed)
        time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Exiting on user request...")
        break
    except Exception as e:
        logger.error("Error in main loop: " + str(e))
        time.sleep(5)

# Cleanup on exit
try:
    dht_sensor.exit()
except Exception:
    pass

device_client.disconnect()
logger.info("Disconnected from Azure IoT Hub. Bye!")
