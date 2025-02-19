import RPi.GPIO as GPIO
import time

BUTTON_PIN = 22  # 你的按钮 GPIO
LED_PIN = 23     # 你的 LED GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 按钮默认上拉
GPIO.setup(LED_PIN, GPIO.OUT)  # LED 设为输出

led_on = False  # 记录 LED 状态
last_press_time = 0  # 记录第一次按下时间

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # 检测按钮按下
            time.sleep(0.1)  # 消抖
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # 再次确认按下
                if not led_on:  # 如果 LED 目前是关闭的
                    GPIO.output(LED_PIN, GPIO.HIGH)  # 打开 LED
                    led_on = True
                    last_press_time = time.time()  # 记录点亮时间
                    print("LED 开启")
                else:
                    GPIO.output(LED_PIN, GPIO.LOW)  # 立即关闭 LED
                    led_on = False
                    print("LED 关闭")

                while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                    time.sleep(0.1)  # 按下时等待，防止重复触发

        # 检查是否超过 5 秒
        if led_on and (time.time() - last_press_time > 5):
            GPIO.output(LED_PIN, GPIO.LOW)  # 超时后熄灭 LED
            led_on = False
            print("LED 自动关闭")

        time.sleep(0.1)  # 让 CPU 休息一下

except KeyboardInterrupt:
    GPIO.cleanup()
