#########################匯入模組#########################
from machine import Pin, ADC, PWM
from time import sleep
import mcu

#########################函式與類別定義#########################
frequency = 1000  # 頻率(Hz)
duty_cycle = 0  # 佔空比(0~1023)
gpio = mcu.gpio()
light_sensor = ADC(0)  # 建立 ADC物件，腳位為ADC0
#########################宣告與設定#########################
RED = PWM(Pin(gpio.D5), freq=frequency, duty=duty_cycle)  # GPIO14，頻率1kHz，佔空比0%
GREEN = PWM(Pin(gpio.D6), freq=frequency, duty=duty_cycle)  # GPIO12，頻率1kHz，佔空比0%
BLUE = PWM(Pin(gpio.D7), freq=frequency, duty=duty_cycle)  # GPIO13，頻率1kHz，佔空比0%
#########################主程式#########################
while True:
    light_sensor_running = light_sensor.read()  # 讀取光敏電阻數值(0~1023)
    RED.duty(light_sensor_running)  # 設定紅色LED的佔空比
    GREEN.duty(light_sensor_running)  # 設定綠色LED的佔空比
    BLUE.duty(light_sensor_running)  # 設定藍色LED的佔空比
    sleep(0.3)  # 延遲0.3秒
