####################匯入模組####################
from machine import Pin, I2C, ADC
import dht
import time
import mcu
import json
import ssd1306

####################宣告與設定####################
gpio = mcu.gpio()
wi = mcu.wifi("Singular_AI", "Singular#1234")
wi.setup(ap_active=False, sta_active=True)
if wi.connect():
    print(f"IP={wi.ip}")

mqtt_client = mcu.MQTT(
    "GG_mcu01",
    "mqtt.singularinnovation-ai.com",
    "singular",
    "Singular#1234",
    30,
)
mqtt_client.connect()

i2c = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))  # GPIO5, GPIO4
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
d = dht.DHT11(Pin(gpio.D0, Pin.IN))  # GPIO16，DHT11感測器
msg_json = {}
adc = ADC(0)  # 建立 ADC物件，腳位為ADC0
####################主程式####################
while True:
    light_value = adc.read()  # 讀取光敏電阻數值(0~1023)
    d.measure()  # 進行測量
    temp = d.temperature()  # 取得溫度值(攝氏)
    hum = d.humidity()  # 取得濕度值(%RH)
    oled.fill(0)  # 清除顯示內容
    oled.text(f"Hum: {hum:02d}%", 0, 0)  # 顯示文字, x=0, y=0
    oled.text(f"Temp: {temp:02d}{'\u00b0'}C", 0, 8)  # 顯示文字, x=0, y=8
    oled.text(f"Light: {light_value}", 0, 16)  # 顯示文字, x=0, y=16
    oled.show()  # 更新顯示內容
    msg_json["humidity"] = hum
    msg_json["temperature"] = temp
    msg_json["light"] = light_value
    msg = json.dumps(msg_json)
    mqtt_client.publish("GG", msg)
    time.sleep(1)  # 每隔1秒鐘測量一次
