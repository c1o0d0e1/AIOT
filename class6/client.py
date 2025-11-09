# PC執行
#########################匯入模組#########################
import socket

#########################函式與類別定義#########################


#########################宣告與設定#########################
client_socket = socket.socket()  # 建立客戶端Socket物件
client_socket.connect(
    ("localhost", 12345)
)  # 連線至伺服器(主機名稱與通訊埠號需與伺服器相同)

#########################主程式#########################
while True:
    msg = input("Input message:")  # 輸入要傳送的訊息
    client_socket.send(msg.encode("utf8"))  # 傳送訊息給伺服器(將字串編碼為utf8格式)
    reply = client_socket.recv(128).decode(
        "utf8"
    )  # 接收來自伺服器的回應訊息，並解碼(128為接收緩衝區大小 utf8為編碼方式)
    if msg == "quit":
        print("Disconnected")
        client_socket.close()  # 關閉與伺服器的連線
        break  # 跳出迴圈，結束程式
    print(reply)
