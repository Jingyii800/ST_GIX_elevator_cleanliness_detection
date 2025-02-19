import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17  
LED_PIN = 18     

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 按钮默认上拉
GPIO.setup(LED_PIN, GPIO.OUT)  # LED 作为输出

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)
        if button_state == GPIO.LOW:  # 按钮按下
            GPIO.output(LED_PIN, GPIO.HIGH)  # 亮灯
        else:
            GPIO.output(LED_PIN, GPIO.LOW)  # 熄灭
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
