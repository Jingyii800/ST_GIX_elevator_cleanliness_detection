import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17  # 按钮接的 GPIO17
LED_PIN = 18     # LED 连接的 GPIO18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)  # LED 设定为输出模式
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 按钮使用上拉电阻

def button_callback(channel):
    print("按钮被按下！")
    GPIO.output(LED_PIN, not GPIO.input(LED_PIN))  # 翻转 LED 状态

# 添加按键监听
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)  # 让 CPU 休息
except KeyboardInterrupt:
    GPIO.cleanup()
