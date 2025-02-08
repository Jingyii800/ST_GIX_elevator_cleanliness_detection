#!/usr/bin/env python3
import time
import statistics
import logging
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# ==========================================
# **Configuration and Constants**
# ==========================================

VCC = 3.3  # Power voltage (adjust to 5V if needed)
RL = 1.0  # Load resistance in kΩ

# Ammonia (NH₃) Constants for MQ2
A = 100  # MQ2 calibration constant from datasheet
B = -1.5  # Power factor

LOG_FILE = "mq2_sensor_log.txt"  # File to store logs
MOVING_AVERAGE_SIZE = 10  # Number of readings for smoothing

# ==========================================
# **Logging Configuration**
# ==========================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", handlers=[
    logging.FileHandler(LOG_FILE),
    logging.StreamHandler()
])

# ==========================================
# **Initialize the MQ2 Sensor (ADS1115)**
# ==========================================

try:
    i2c = busio.I2C(board.SCL, board.SDA)
except Exception as e:
    logging.error("Failed to initialize I2C: " + str(e))
    exit(1)

try:
    ads = ADS.ADS1115(i2c)
    ads.gain = 2/3  # Increased sensitivity
    mq2_channel = AnalogIn(ads, ADS.P0)
    logging.info("✅ ADS1115 (MQ2 sensor) initialized.")
except Exception as e:
    logging.error("Failed to initialize ADS1115: " + str(e))
    exit(1)

# ==========================================
# **Sensor Calibration (Calculate R0)**
# ==========================================
def calibrate_r0():
    """Calibrate MQ2 sensor baseline resistance (R0) in clean air."""
    readings = []
    logging.info("🔄 Calibrating MQ2 sensor in clean air... (Wait 10 sec)")

    for _ in range(50):  # Take 50 samples over 10 sec
        voltage = mq2_channel.voltage
        rs = calculate_rs(voltage)
        if rs:
            readings.append(rs)
        time.sleep(0.2)

    r0 = statistics.mean(readings)  # Compute average R0
    logging.info(f"✅ Calibration complete! R0 = {r0:.3f} kΩ")
    return r0

def calculate_rs(voltage):
    """Convert MQ2 voltage to Rs (sensor resistance)."""
    if voltage <= 0:
        return None  # Avoid division by zero
    rs = ((VCC / voltage) - 1) * RL  # Rs calculation
    return rs

def calculate_ppm(voltage, r0):
    """Convert MQ2 voltage to gas concentration in ppm."""
    rs = calculate_rs(voltage)
    if not rs:
        return None

    ratio = rs / r0  # Rs/R0 ratio
    ppm = A * (ratio ** B)  # Apply gas equation
    return ppm

# Perform initial calibration
R0 = calibrate_r0()

# **Moving Average Buffer**
recent_readings = []

# ==========================================
# **Main Sensor Loop (Logs to File)**
# ==========================================
logging.info("📡 Starting MQ2 sensor monitoring... Press Ctrl+C to exit.")

try:
    while True:
        voltage = mq2_channel.voltage
        ammonia_ppm = calculate_ppm(voltage, R0)

        # Apply Moving Average Smoothing
        recent_readings.append(ammonia_ppm)
        if len(recent_readings) > MOVING_AVERAGE_SIZE:
            recent_readings.pop(0)

        smoothed_ppm = statistics.mean(recent_readings)

        # **Logging Output**
        if smoothed_ppm < 5:
            status = "🟢 Clean Air"
        elif smoothed_ppm < 50:
            status = "🟡 Moderate Air Quality"
        else:
            status = "🔴 High Ammonia Levels Detected!"

        log_message = f"{status}: {smoothed_ppm:.2f} ppm"
        logging.info(log_message)

        # Wait before next reading
        time.sleep(2)

except KeyboardInterrupt:
    logging.info("🛑 Exiting MQ2 monitoring...")
