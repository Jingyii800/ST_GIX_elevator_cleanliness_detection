import RPi.GPIO as GPIO
import time

BUTTON_PIN = 22  # 你的按钮连接的 GPIO

GPIO.setmode(GPIO.BCM)  # 采用 BCM 编号
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 按钮默认上拉

press_count = 0  # 记录按钮按下次数
last_press_time = 0  # 记录上次按下时间
double_click_threshold = 0.5  # 0.5 秒内按两次认为是“双击”

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # 按钮被按下
            current_time = time.time()
            
            if (current_time - last_press_time) < double_click_threshold:
                press_count += 1
            else:
                press_count = 1
            
            last_press_time = current_time

            if press_count == 1:
                print(1)  # 单击
            elif press_count == 2:
                print(2)  # 双击
            
            time.sleep(0.3)  # 消抖

        time.sleep(0.1)  # 让 CPU 休息
except KeyboardInterrupt:
    GPIO.cleanup()
