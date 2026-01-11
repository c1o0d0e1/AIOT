####################匯入模組####################
from machine import Pin, I2C, ADC
import dht
import time
import mcu
import json
import ssd1306


####################函式與類別定義####################
def on_message(topic, msg):
    global m
    msg = msg.decode("utf-8")  # Bytos 轉 string
    topic = topic.decode("utf-8")
    print(f"my subscribe topic:{topic}, msg:{msg}")
    m = msg


####################宣告與設定####################
gpio = mcu.gpio()
wi = mcu.wifi("Singular_AI", "Singular#1234")
wi.setup(ap_active=False, sta_active=True)
if wi.connect():
    print(f"IP={wi.ip}")

# 連接 MQTT 伺服器
mqtt_client = mcu.MQTT(
    "GG", "mqtt.singularinnovation-ai.com", "singular", "Singular#1234", 60
)
mqtt_client.connect()
mqtt_client.subscribe("GG_ai", on_message)
m = ""

i2c = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))  # GPIO5, GPIO4
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
d = dht.DHT11(Pin(gpio.D0, Pin.IN))  # GPIO16，DHT11感測器
msg_json = {}
adc = ADC(0)  # 建立 ADC物件，腳位為ADC0
LED = mcu.LED(gpio.D5, gpio.D6, gpio.D7)  # 建立 LED 物件，腳位為GPIO5, GPIO6, GPIO7
mp3 = mcu.MP3()  # 建立 MP3 物件

####################主程式####################
try:
    while True:
        light_value = adc.read()  # 讀取光敏電阻數值(0~1023)
        d.measure()  # 進行測量
        temp = d.temperature()  # 取得溫度值(攝氏)
        hum = d.humidity()  # 取得濕度值(%RH)
        oled.fill(0)  # 清除顯示內容
        oled.text(f"Hum: {hum:02d}%", 0, 0)  # 顯示文字, x=0, y=0
        oled.text(f"Temp: {temp:02d}C", 0, 8)  # 顯示文字, x=0, y=8
        oled.text(f"Light: {light_value}", 0, 16)  # 顯示文字, x=0, y=16
        oled.show()  # 更新顯示內容
        msg_json["humidity"] = hum
        msg_json["temperature"] = temp
        msg_json["light"] = light_value
        msg = json.dumps(msg_json)
        mqtt_client.publish("GG", msg)
        mqtt_client.check_msg()  # 檢查是否有收到訂閱的訊息
        time.sleep(1)  # 每隔1秒鐘測量一次

        if m == "ON":
            LED.LED_open(1, 1, 1)
        elif m == "OFF":
            LED.LED_open(0, 0, 0)

        # 播放音樂範例
        if "alert" in m or temp > 38:
            mp3.start(volume=100, song=1)  # 播放 alert.mp3 音樂檔案
            time.sleep(3)  # 播放5秒
            m = ""  # 播放後清除指令

        if m == "break":
            break

        time.sleep(1)
except KeyboardInterrupt:
    pass
