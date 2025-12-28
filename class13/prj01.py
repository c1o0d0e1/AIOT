####################匯入模組####################
from machine import Pin
import dht
import time
import mcu

####################宣告與設定####################
gpio = mcu.gpio()
d = dht.DHT11(Pin(gpio.D0, Pin.IN))  # GPIO16，DHT11感測器

####################主程式####################
while True:
    d.measure()  # 進行測量
    temp = d.temperature()  # 取得溫度值(攝氏)
    hum = d.humidity()  # 取得濕度值(%RH)
    print(f"Humidity: {hum:02d}%, Temperature: {temp:02d}{'\u00b0'}C")
    time.sleep(1)  # 每隔1秒鐘測量一次
