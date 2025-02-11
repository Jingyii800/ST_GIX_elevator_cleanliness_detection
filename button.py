import RPi.GPIO as GPIO
import time

BUTTON_PIN = 26  # 按钮连接的 GPIO 引脚
LED_PIN = 16     # LED 连接的 GPIO 引脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 设置按钮为输入，并启用上拉电阻
GPIO.setup(LED_PIN, GPIO.OUT)  # 设置 LED 为输出

led_state = False  # 记录 LED 状态（初始为关闭）

def button_callback(channel):
    global led_state
    led_state = not led_state  # 切换 LED 状态
    GPIO.output(LED_PIN, led_state)  # 更新 LED 状态
    print("LED status:", "1" if led_state else "0")

# 监听按钮按下（下降沿触发）
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)  # 避免 CPU 占用过高
except KeyboardInterrupt:
    GPIO.cleanup()  # 清理 GPIO 设置
