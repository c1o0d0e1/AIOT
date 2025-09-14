##########匯入模組##########

from machine import Pin, PWM
from time import sleep


##########宣告與設定##########

frequency = 1000  # 頻率(Hz)
duty_cycle = 0  # 佔空比(0~1023)
led = PWM(Pin(2), freq=frequency, duty=duty_cycle)  # GPIO2，頻率1kHz，佔空比0%


##########主程式##########

while True:
    led.duty(0)  # 設定佔空比
    sleep(2)  # 延遲2秒
    led.duty(256)  # 設定佔空比
    sleep(2)  # 延遲2秒
    led.duty(1023)  # 設定佔空比
    sleep(2)  # 延遲2秒
