#!/usr/bin/env python3
"""
This script reads data from multiple sensors:
  - MQ135 air quality sensor (via ADS1115 on channel A0)
  - DHT22 temperature/humidity sensor (GPIO4)
  - A button (GPIO17)
  - An RFID RC522 module (using SimpleMFRC522)
  
It sends the collected data as JSON messages to Azure IoT Hub.
"""

import os
import sys
import time
import json
import logging
import datetime
import RPi.GPIO as GPIO
import statistics

import board
import busio
import digitalio
import importlib.util

# Define the absolute path to screen.py
screen_path = "/home/pi/development/e-Paper/screen/python/examples/screen.py"

# Load the screen module dynamically
spec = importlib.util.spec_from_file_location("screen", screen_path)
screen = importlib.util.module_from_spec(spec)
sys.modules["screen"] = screen
spec.loader.exec_module(screen)

import adafruit_dht
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from mfrc522 import SimpleMFRC522  # RFID Reader
from azure.iot.device import IoTHubDeviceClient, Message
import atexit

# ==========================================
# Configuration & Azure IoT Hub Connection
# ==========================================

IOTHUB_CONNECTION_STRING = "HostName=elevatorCleanlinessDetector.azure-devices.net;DeviceId=ElevatorDetector;SharedAccessKey=lrTZ47/DX3nWRc4kPtILKfqFf22+7+ojF+7L9GpihnY="

STATION = "University of Washington"
ELEVATOR_NUM = 7

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

try:
    i2c = busio.I2C(board.SCL, board.SDA)
except Exception as e:
    logger.error("Failed to initialize I2C: " + str(e))
    exit(1)

# (1) ADS1115 for MQ-135 sensor (air quality)
try:
    ads = ADS.ADS1115(i2c)
    ads.gain = 1  # Increased sensitivity
    mq135_channel = AnalogIn(ads, ADS.P0)
    logger.info("ADS1115 (MQ-135 sensor) initialized.")
except Exception as e:
    logger.error("Failed to initialize ADS1115: " + str(e))
    exit(1)

# **MQ-135 Sensor Constants for NH₃ (Ammonia)**
VCC = 3.3  # Raspberry Pi power voltage
RL = 1.0  # Load resistance in kΩ (check datasheet)

A = 116.6020682  # MQ-135 calibration constant
B = -2.769034857  # Power factor

# **🔹 Step 1: Baseline Calibration (R0 in Clean Air)**
def calibrate_r0():
    """Calibrate MQ-135 sensor baseline R0 in clean air."""
    readings = []
    logger.info("Calibrating MQ-135 sensor in clean air... (Wait 10 sec)")

    for _ in range(50):  # Collect 50 samples over 10 sec
        voltage = mq135_channel.voltage
        rs = calculate_rs(voltage)
        if rs:
            readings.append(rs)
        time.sleep(0.2)

    r0 = statistics.mean(readings)  # Compute average R0
    logger.info(f"✅ Calibration complete! R0 = {r0:.3f} kΩ")
    return r0

def calculate_rs(voltage):
    """Convert MQ-135 voltage to Rs (sensor resistance)."""
    if voltage <= 0:
        return None  # Avoid division by zero
    rs = ((VCC / voltage) - 1) * RL  # Rs calculation
    return rs

def calculate_ppm(voltage, r0):
    """Convert MQ-135 voltage to NH₃ concentration in ppm."""
    rs = calculate_rs(voltage)
    if not rs:
        return None

    ratio = rs / r0  # Rs/R0 ratio
    ppm = A * (ratio ** B)  # Apply gas equation
    return ppm

# Perform calibration at startup
R0 = calibrate_r0()

# (2) DHT22 sensor on GPIO4
try:
    dht_sensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    logger.info("DHT22 sensor initialized on GPIO4.")
except Exception as e:
    logger.error("Failed to initialize DHT22 sensor: " + str(e))
    exit(1)
# Function to read DHT22 sensor with retry logic
def read_dht_sensor():
    max_retries = 5  # Number of retries before giving up
    retries = 0
    last_valid_humidity = None
    last_valid_temperature = None

    while retries < max_retries:
        try:
            humidity = dht_sensor.humidity
            temperature = dht_sensor.temperature

            # Check if the values are valid (not None and not 0)
            if humidity is not None and temperature is not None and humidity > 0:
                last_valid_humidity = humidity
                last_valid_temperature = temperature
                return humidity, temperature

            logger.warning(f"DHT22 read error: Invalid data received. Retry {retries + 1}/{max_retries}")
            retries += 1
            time.sleep(2)  # Delay before retrying

        except RuntimeError as e:
            logger.warning(f"DHT22 read error: {str(e)}. Retry {retries + 1}/{max_retries}")
            retries += 1
            time.sleep(2)

    # If retries fail, return last valid readings or default values
    logger.error("DHT22 sensor failed to read valid data after retries.")
    return last_valid_humidity if last_valid_humidity else 0, last_valid_temperature if last_valid_temperature else 0


# (3) Button on GPIO17
BUTTON_PIN = 22  # Button GPIO
LED_PIN = 23  # LED GPIO

led_on = False
last_press_time = 0
confirm_report = False
button_state = 0
button_val = 0  # 0: Default screen, 1: Confirm screen, 2: Reported screen
screen.show_default()  # Start with default display

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
logger.info("Button initialized on GPIO22.")


# (4) RFID RC522 module
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
def cleanup_gpio():
    GPIO.cleanup()
    print("GPIO cleaned up.")
# ==========================================
# Main Loop: Read Sensors and Send Data
# ==========================================
logger.info("Starting main sensor loop. Press Ctrl+C to exit.")

while True:
    try:
        # --- Read DHT22 Sensor ---
        try:
            humidity, temperature_c = read_dht_sensor()
        except RuntimeError as e:
            logger.warning("DHT22 read error: " + str(e))
            humidity = None
            temperature_c = None

        # --- Read MQ-135 Sensor ---
        try:
            mq135_voltage = mq135_channel.voltage
            ammonia_ppm = calculate_ppm(mq135_voltage, R0)
            logger.info(f"MQ-135 Voltage: {mq135_voltage:.3f}V, Ammonia: {ammonia_ppm:.2f} ppm")
        except Exception as e:
            logger.error("MQ-135 sensor read error: " + str(e))
            ammonia_ppm = None

        # --- Read Button ---
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # 检测按钮按下
            if button_state == 0:
                GPIO.output(LED_PIN, GPIO.HIGH)
                screen.show_confirm()
                button_state = 1
                logging.info("Button pressed: 1" )
            elif button_state == 1:
                screen.show_reported()
                GPIO.output(LED_PIN, GPIO.LOW)
                button_state = 0
                button_val = 1
                time.sleep(2)
                screen.show_default()
                logging.info("Button pressed: 2")

        # RFID Logic


        # --- Prepare Sensor Data Payload ---
        sensor_payload = {
            "station": STATION,
            "elevator_num": ELEVATOR_NUM,
            "sensor": {
                "humidity": humidity if humidity is not None else 0,
                "temperature": temperature_c if temperature_c is not None else 0,
                "airQuality": ammonia_ppm if ammonia_ppm is not None else 0,
                "button": button_val
            },
            "time": datetime.datetime.utcnow().isoformat() + "Z"
        }

        send_message_to_iothub(sensor_payload)
        button_val = 0  # Reset button after reporting
        time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Exiting on user request...")
        break
    except Exception as e:
        logger.error("Error in main loop: " + str(e))
        time.sleep(5)

device_client.disconnect()
atexit.register(cleanup_gpio)
logger.info("Disconnected from Azure IoT Hub. Bye!")
