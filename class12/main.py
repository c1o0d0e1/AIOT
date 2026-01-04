#########################匯入模組#########################
from umqtt.simple import MQTTClient
import sys
import time
import class13.mcu as mcu
from machine import Pin, I2C
from machine import ADC
import ssd1306


#########################函式與類別定義#########################
def on_message(topic, msg):
    global m
    msg = msg.decode("utf8")
    topic = topic.decode("utf8")
    print(f"my subscribed topic:{topic}, received message:{msg}")
    m = msg


def display_message(init_y, msg):
    max_chars_per_line = 16  # 每行最大字元數
    for m in range(0, len(msg), max_chars_per_line):
        line = msg[m : m + max_chars_per_line]
        y_position = (m // max_chars_per_line) * 8
        oled.text(line, 0, init_y + y_position)


#########################宣告與設定#########################
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("Singular_AI", "Singular#1234"):
    print(f"IP={wi.ip}")

mq_server = "mqtt.singularinnovation-ai.com"
mqttClientId = "GG_mcu01"
mqtt_username = "singular"  # 使用者名稱
mqtt_password = "Singular#1234"  # 密碼
mqtt = mcu.MQTT(mqttClientId, mq_server, mqtt_username, mqtt_password, keepalive=30)

mqtt.connect()


mqtt.subscribe("GG", on_message)  # 訂閱主題("GG")


gpio = mcu.gpio()
LED = mcu.LED(gpio.D5, gpio.D6, gpio.D7, pwm=False)
LED.LED_open(0, 0, 0)  # 紅色LED熄滅，綠色LED熄滅，藍色LED熄滅
light_sensor = ADC(0)  # 建立 ADC物件，腳位為ADC0
m = ""
ic2 = I2C(scl=Pin(gpio.D1), sda=Pin(gpio.D2))
oled = ssd1306.SSD1306_I2C(128, 64, ic2)
#########################主程式#########################
while True:
    oled.fill(0)
    oled.text(f"IP={wi.ip}", 0, 0)
    oled.text("topic:GG", 0, 8)
    display_message(16, f"msg:{m}")
    oled.show()
    if m == "on":
        LED.LED_open(1, 1, 1)  # 紅色LED開啟，綠色LED開啟，藍色LED開啟
    elif m == "off":
        LED.LED_open(0, 0, 0)  # 紅色LED熄滅，綠色LED熄滅，藍色LED熄滅
    elif m == "auto":
        if light_sensor.read() < 700:
            LED.LED_open(1, 1, 1)  # 紅色LED開啟，綠色LED開啟，藍色LED開啟
        else:
            LED.LED_open(0, 0, 0)  # 紅色LED熄滅，綠色LED熄滅，藍色LED熄滅
    # 查看是否有訂閱主題發布的資料
    mqtt.check_msg()
    time.sleep(0.1)  # 延遲0.1秒
