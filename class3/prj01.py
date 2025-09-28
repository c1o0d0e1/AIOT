#########################匯入模組#########################
from machine import Pin, ADC, PWM
from time import sleep
import mcu

#########################函式與類別定義#########################
gpio = mcu.gpio()
light_sensor = ADC(0)  # 建立 ADC物件，腳位為ADC0
#########################宣告與設定#########################
RED = Pin(gpio.D5, Pin.OUT)  # GPIO14，紅色LED
GREEN = Pin(gpio.D6, Pin.OUT)  # GPIO12，綠色LED
BLUE = Pin(gpio.D7, Pin.OUT)  # GPIO13，藍色LED

RED.value(0)  # 紅色LED熄滅
BLUE.value(0)  # 藍色LED熄滅
GREEN.value(0)  # 綠色LED熄滅

#########################主程式#########################
while True:
    light_sensor_running = light_sensor.read()  # 讀取光敏電阻數值(0~1023)
    if light_sensor_running < 700:  # 光線較暗
        RED.value(0)  # 紅色LED熄滅
        BLUE.value(0)  # 藍色LED熄滅
        GREEN.value(0)  # 綠色LED熄滅
    else:  # 光線較亮
        RED.value(1)  # 紅色LED熄滅
        BLUE.value(1)  # 藍色LED熄滅
        GREEN.value(1)  # 綠色LED熄滅
