#########################匯入模組#########################
import paho.mqtt.client as mqtt


#########################函式與類別定義#########################
def on_connect(client, userdata, connect_flags, connect_code, properties):
    print(f"連線結果:{connect_code}")
    client.subscribe("GG")  # 訂閱主題("GG")


def on_message(client, userdata, msg):
    print(f"我訂閱的主題:{msg.topic}, 訊息內容(收到訊息):{msg.payload.decode('utf8')}")


#########################宣告與設定#########################
# 建立MQTT客戶端物件
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
# 設定連線完成的事件處理函式(回顧函數:on_connect)
client.on_connect = on_connect
# 設定收到訊息的事件處理函式(回顧函數:on_message)
client.on_message = on_message
# 設定使用者名稱與密碼(若無可省略此行)
client.username_pw_set("singular", "Singular#1234")
# 連線至MQTT伺服器
client.connect("mqtt.singularinnovation-ai.com", 1883, 60)
# 保持連線
client.loop_forever()
#########################主程式#########################
