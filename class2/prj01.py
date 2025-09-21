#########################匯入模組#########################
from machine import Pin
from time import sleep
import mcu

#########################函式與類別定義#########################

#########################宣告與設定#########################
gpio = mcu.gpio()
RED = Pin(gpio.D5, Pin.OUT)  # GPIO14，紅色LED
GREEN = Pin(gpio.D6, Pin.OUT)  # GPIO12，綠色LED
BLUE = Pin(gpio.D7, Pin.OUT)  # GPIO13，藍色LED

RED.value(0)  # 紅色LED熄滅
BLUE.value(0)  # 藍色LED熄滅
GREEN.value(0)  # 綠色LED熄滅
#########################主程式#########################
while True:
    GREEN.value(1)  # 綠色LED亮
    sleep(1)  # 延遲1秒
    GREEN.value(0)  # 綠色LED熄滅
    RED.value(1)
    GREEN.value(1)
    # 紅色LED與綠色LED同時亮
    sleep(1)  # 延遲1秒
    RED.value(0)
    GREEN.value(0)
    # 紅色LED與綠色LED同時熄滅
    RED.value(1)  # 紅色LED亮
    sleep(1)  # 延遲1秒
    RED.value(0)  # 紅色LED熄滅
