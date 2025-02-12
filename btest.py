import RPi.GPIO as GPIO
import time

BUTTON_PIN = 27  # 按钮连接的 GPIO 引脚
LED_PIN = 16     # LED 连接的 GPIO 引脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)  # ❌ 不使用内部上拉/下拉电阻
GPIO.setup(LED_PIN, GPIO.OUT)  # 设置 LED 为输出

led_state = False  # 初始 LED 状态

def button_callback(channel):
    global led_state
    led_state = not led_state  # 切换 LED 状态
    GPIO.output(LED_PIN, led_state)
    print("LED status:", "1111" if led_state else "000")

try:
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

    while True:
        time.sleep(0.1)  # 避免 CPU 过载
except KeyboardInterrupt:
    GPIO.cleanup()  # 释放 GPIO 资源
    print("GPIO 清理完成，程序退出。")
