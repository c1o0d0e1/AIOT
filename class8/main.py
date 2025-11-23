#########################匯入模組#########################
from umqtt.simple import MQTTClient
import sys
import time
import mcu
from machine import Pin
from machine import Pin, ADC, PWM

gpio = mcu.gpio()
RED = Pin(gpio.D5, Pin.OUT)  # GPIO14，紅色LED
GREEN = Pin(gpio.D6, Pin.OUT)  # GPIO12，綠色LED
BLUE = Pin(gpio.D7, Pin.OUT)  # GPIO13，藍色LED


#########################函式與類別定義#########################
def light_control():
    light_sensor = ADC(0)  # 建立 ADC物件，腳位為ADC0
    light_sensor_running = light_sensor.read()  # 讀取光敏電阻數值(0~1023)
    if light_sensor_running < 700:  # 光線較暗
        RED.value(0)  # 紅色LED熄滅
        BLUE.value(0)  # 藍色LED熄滅
        GREEN.value(0)  # 綠色LED熄滅
    else:  # 光線較亮
        RED.value(1)  # 紅色LED熄滅
        BLUE.value(1)  # 藍色LED熄滅
        GREEN.value(1)  # 綠色LED熄滅


def on_message(topic, msg):
    msg = msg.decode("utf8")
    topic = topic.decode("utf8")
    print(f"my subscribed topic:{topic}, received message:{msg}")
    if msg == "auto":
        light_control()
    elif msg == "on":
        RED.value(1)  # 紅色LED亮
        GREEN.value(1)  # 綠色LED亮
        BLUE.value(1)  # 藍色LED亮
    elif msg == "off":
        RED.value(0)  # 紅色LED熄滅
        GREEN.value(0)  # 綠色LED熄滅
        BLUE.value(0)  # 藍色LED熄滅


#########################宣告與設定#########################
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("Singular_AI", "Singular#1234"):
    print(f"IP={wi.ip}")

mq_server = "mqtt.singularinnovation-ai.com"
mqttClientId = "GG_mcu01"
mqtt_username = "singular"  # 使用者名稱
mqtt_password = "Singular#1234"  # 密碼
mqClient0 = MQTTClient(
    mqttClientId,
    mq_server,
    user=mqtt_username,
    password=mqtt_password,
    keepalive=30,
)

try:
    mqClient0.connect()
except:
    sys.exit()
finally:
    print("Connected MQTT server")


mqClient0.set_callback(on_message)  # 設定收到訊息的回呼函式
mqClient0.subscribe("GG")  # 訂閱主題("GG")

#########################主程式#########################
while True:
    # 查看是否有訂閱主題發布的資料
    mqClient0.check_msg()  # 等待已訂閱的主題發送資料
    mqClient0.ping()  # 持續確認與伺服器的連線狀態(是否連線)
    time.sleep(0.1)  # 延遲0.1秒
