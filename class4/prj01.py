#########################匯入模組#########################
import network

#########################函式與類別定義#########################
"""
50.148.連接WiFi範例程式
本程式會搜尋附近的無線網路，並連接到指定的WiFi熱點。
"""
#########################宣告與設定#########################
wlan = network.WLAN(network.STA_IF)  # 建立 WLAN 物件，設定為站台模式 (初始化 STA 模式)
ap = network.WLAN(network.AP_IF)  # 建立 WLAN 物件，設定為存取點模式 (初始化 AP 模式)
ap.active(False)  # 關閉存取點模式
wlan.active(True)  # 啟用站台模式

# 搜尋附近的無線網路（搜尋 AP）
wifi_list = wlan.scan()
print("Scan results: ")
for i in range(len(wifi_list)):
    print(wifi_list[i])

# 選擇要連接的wifi
wlSSID = "Singular_AI"
wlPWD = "Singular#1234"
wlan.connect(wlSSID, wlPWD)  # 連接到指定的無線網路
while not wlan.isconnected():  # 等待連接成功
    pass
print("connet successfully", wlan.ifconfig())  # 顯示網路設定(顯示連接成功的 IP 位址)s
while True:
    pass
#########################主程式#########################
