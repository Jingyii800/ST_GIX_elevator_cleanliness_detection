import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17  # 按钮连接的 GPIO 引脚
LED_PIN = 18     # LED 连接的 GPIO 引脚

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 确保先设置引脚模式
GPIO.setup(LED_PIN, GPIO.OUT)  # 设置 LED 为输出

led_state = False  # 初始 LED 状态

def button_callback(channel):
    global led_state
    led_state = not led_state  # 切换 LED 状态
    GPIO.output(LED_PIN, led_state)
    print("LED 状态:", "亮" if led_state else "灭")

# 🛑 确保 setup 代码先执行后，再调用 add_event_detect
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)  # 避免 CPU 过载
except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO 清理完成，程序退出。")
