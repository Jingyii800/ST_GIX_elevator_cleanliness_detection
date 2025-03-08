import RPi.GPIO as GPIO
import time

LED_PIN = 18  # 连接到 LED+ 的 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # 亮灯
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)   # 熄灭
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
