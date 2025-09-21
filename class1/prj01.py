##########匯入模組##########

from machine import Pin, PWM
from time import sleep


##########宣告與設定##########

frequency = 1000  # 頻率(Hz)
duty_cycle = 0  # 佔空比(0~1023)
led = PWM(Pin(2), freq=frequency, duty=duty_cycle)  # GPIO2，頻率1kHz，佔空比0%


##########主程式##########
"""
while True:
    led.duty(0)  # 設定佔空比 最亮
    sleep(2)  # 延遲2秒
    led.duty(700)  # 設定佔空比
    sleep(2)  # 延遲2秒
    led.duty(1023)  # 設定佔空比
    sleep(2)  # 延遲2秒
"""

# 呼吸燈:
while True:
    for duty_cycle in range(1023, -1, -1):  # 由暗到亮
        led.duty(duty_cycle)
        sleep(0.01)
    for duty_cycle in range(1024):  # 由亮到暗
        led.duty(duty_cycle)
        sleep(0.01)
