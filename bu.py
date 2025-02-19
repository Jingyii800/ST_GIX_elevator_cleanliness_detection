import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17
LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # 按钮按下
            print("按钮被按下！")
            GPIO.output(LED_PIN, not GPIO.input(LED_PIN))  # 翻转 LED
            time.sleep(0.3)  # 消抖
        time.sleep(0.1)  # CPU 休息
except KeyboardInterrupt:
    GPIO.cleanup()
