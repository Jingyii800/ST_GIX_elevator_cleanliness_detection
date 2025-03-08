import sys
import time
from waveshare_epd import epd7in5_V2  # 确保你安装了 waveshare 的 Python 库

try:
    print("Clearing E-Paper Display...")
    
    # 初始化屏幕
    epd = epd7in5_V2.EPD()
    epd.init()
    
    # 清空屏幕（填充为白色）
    epd.Clear()
    
    # 休眠模式（省电）
    epd.sleep()
    
    print("E-Paper Clear Done!")

except IOError as e:
    print(f"IOError: {e}")

except KeyboardInterrupt:
    print("Process interrupted.")
    sys.exit(0)
