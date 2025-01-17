import time
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn
import busio
import digitalio
from board import SCK, MISO, MOSI, CE0

# Create the SPI bus
spi = busio.SPI(clock=SCK, MISO=MISO, MOSI=MOSI)

# Create the chip select
cs = digitalio.DigitalInOut(CE0)

# Create the MCP3008 object
mcp = MCP3008(spi, cs)

# Create an analog input channel for the MQ2 sensor
mq2_channel = AnalogIn(mcp, MCP3008.P0)  # Use channel 0 (CH0)

# Function to calculate approximate gas concentration
def calculate_gas_concentration(voltage):
    # Customize based on MQ2 datasheet and your setup
    ratio = voltage / 3.3  # Assuming 3.3V reference voltage
    return ratio * 100  # Scale to percentage or other units as needed

print("Reading MQ2 sensor...")
try:
    while True:
        # Read the voltage from the MQ2 sensor
        voltage = mq2_channel.voltage
        gas_concentration = calculate_gas_concentration(voltage)
        
        # Display results
        print(f"Voltage: {voltage:.2f} V")
        print(f"Gas Concentration: {gas_concentration:.2f}%")
        
        # Wait 1 second before next reading
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped.")

# import time
# from adafruit_mcp3xxx.mcp3008 import MCP3008
# from adafruit_mcp3xxx.analog_in import AnalogIn
# import busio
# import digitalio
# from board import SCK, MISO, MOSI, CE0

# # Create the SPI bus
# spi = busio.SPI(clock=SCK, MISO=MISO, MOSI=MOSI)

# # Create the chip select
# cs = digitalio.DigitalInOut(CE0)

# # Create the MCP3008 object
# mcp = MCP3008(spi, cs)

# # Create an analog input channel for the MQ2 sensor
# mq2_channel = AnalogIn(mcp, MCP3008.P0)  # Use channel 0 (CH0)

# # Baseline calibration (update these values based on calibration)
# CLEAN_AIR_VOLTAGE = 0.2  # Voltage in clean air (update after calibration)
# URINE_THRESHOLD_VOLTAGE = 0.5  # Threshold for detecting urine-like gas

# def detect_urine(voltage):
#     """
#     Determine if the gas levels suggest the presence of urine.
#     Returns True if above threshold, False otherwise.
#     """
#     if voltage > URINE_THRESHOLD_VOLTAGE:
#         return True
#     return False

# print("Starting urine detection...")
# try:
#     while True:
#         # Read the voltage from the MQ2 sensor
#         voltage = mq2_channel.voltage
        
#         # Determine if urine is detected
#         urine_detected = detect_urine(voltage)
        
#         if urine_detected:
#             print(f"Urine-like gas detected! Voltage: {voltage:.2f} V")
#         else:
#             print(f"No unusual gas detected. Voltage: {voltage:.2f} V")
        
#         # Wait 1 second before next reading
#         time.sleep(1)

# except KeyboardInterrupt:
#     print("\nProgram stopped.")
