#########################匯入模組#########################
from umqtt.simple import MQTTClient
import sys
import time
import mcu


#########################函式與類別定義#########################
def on_message(topic, msg):
    msg = msg.decode("utf8")
    topic = topic.decode("utf8")
    print(f"my subscribed topic:{topic}, received message:{msg}")


#########################宣告與設定#########################
wi = mcu.wifi()
wi.setup(ap_active=False, sta_active=True)
if wi.connect("Singular_ai", "Singular#1234"):
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
