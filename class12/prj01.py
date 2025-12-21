#########################匯入模組###########################
import time
import mcu
from machine import Pin
from machine import ADC, PWM

#########################宣告與設定#########################
wi = mcu.wifi("Singular_AI", "Singular#1234")
wi.setup(ap_active=False, sta_active=True)
if wi.connect():
    print(f"IP={wi.ip}")
mqtt_client = mcu.MQTT(
    "GG_mcu01",
    "mqtt.singularinnovation-ai.com",
    "singular",
    "Singular#1234",
    keepalive=30,
)
mqtt_client.connect()
gpio = mcu.gpio()
RED = Pin(gpio.D5, Pin.OUT)  # GPIO14，紅色LED
GREEN = Pin(gpio.D6, Pin.OUT)  # GPIO12，綠色LED
BLUE = Pin(gpio.D7, Pin.OUT)  # GPIO13，藍色LED
##########################主程式#########################
while True:
    light_sensor = ADC(0)  # 建立 ADC物件，腳位為ADC0
    light_sensor_running = light_sensor.read()  # 讀取光敏電阻數值(0~1023)
    # msg = input("please input the message to publish to topic 'GG': ")
    mqtt_client.publish("GG", str(light_sensor_running))
    time.sleep(1)
