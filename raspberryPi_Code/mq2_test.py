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

VCC = 3.3  # Power voltage (use 5V if applicable)
RL = 1.0  # Load resistance in kΩ (check datasheet, 10kΩ recommended)

# MQ-135 Calibration Constants for Ammonia (NH₃)
A = 116.6020682  # Calibration constant from datasheet
B = -2.769034857  # Power factor

LOG_FILE = "mq135_sensor_log.txt"  # File to store logs
MOVING_AVERAGE_SIZE = 10  # Number of readings for smoothing

# ==========================================
# **Logging Configuration**
# ==========================================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", handlers=[
    logging.FileHandler(LOG_FILE),
    logging.StreamHandler()
])

# ==========================================
# **Initialize the MQ-135 Sensor (ADS1115)**
# ==========================================

try:
    i2c = busio.I2C(board.SCL, board.SDA)
except Exception as e:
    logging.error("Failed to initialize I2C: " + str(e))
    exit(1)

try:
    ads = ADS.ADS1115(i2c)
    ads.gain = 2/3  # Increased sensitivity
    mq135_channel = AnalogIn(ads, ADS.P0)
    logging.info("✅ ADS1115 (MQ-135 sensor) initialized.")
except Exception as e:
    logging.error("Failed to initialize ADS1115: " + str(e))
    exit(1)

# ==========================================
# **Sensor Calibration (Calculate R0)**
# ==========================================
def calibrate_r0():
    """Calibrate MQ-135 sensor baseline resistance (R0) in clean air."""
    readings = []
    logging.info("🔄 Calibrating MQ-135 sensor in clean air... (Wait 10 sec)")

    for _ in range(50):  # Take 50 samples over 10 sec
        voltage = mq135_channel.voltage
        rs = calculate_rs(voltage)
        if rs:
            readings.append(rs)
        time.sleep(0.2)

    r0 = statistics.mean(readings)  # Compute average R0
    logging.info(f"✅ Calibration complete! R0 = {r0:.3f} kΩ")
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

# Perform initial calibration
R0 = calibrate_r0()

# **Moving Average Buffer**
recent_readings = []

# ==========================================
# **Main Sensor Loop (Logs to File)**
# ==========================================
logging.info("📡 Starting MQ-135 sensor monitoring... Press Ctrl+C to exit.")

try:
    while True:
        voltage = mq135_channel.voltage
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
        time.sleep(5)

except KeyboardInterrupt:
    logging.info("🛑 Exiting MQ-135 monitoring...")
