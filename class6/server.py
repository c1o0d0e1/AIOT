# PC執行
#########################匯入模組#########################
import socket

#########################函式與類別定義#########################
host = "localhost"  # 設定主機名稱
port = 12345  # 設定通訊埠號(與客戶端相同)
server_socket = socket.socket()  # 建立伺服器端Socket物件
server_socket.bind((host, port))  # 綁定主機名稱與通訊埠號
server_socket.listen(5)  # 開始監聽連線請求，參數為允許佇列的最大連線數
print(f"server: {host} , port: {port} start")  # 顯示伺服器啟動訊息(IP與Port)
client, addr = server_socket.accept()  # 等待並接受來自客戶端的連線請求
print(
    f"cliient address: {addr[0]} port: {addr[1]} connected"
)  # 顯示已連線的客戶端資訊(IP與Port)

#########################宣告與設定#########################

#########################主程式#########################
while True:
    msg = client.recv(128).decode(
        "utf8"
    )  # 接收來自客戶端的訊息，並解碼(128為接收緩衝區大小 utf8為編碼方式)
    print(f"Receive message: {msg}")  # 顯示接收到的訊息
    reply = " "  # 建立伺服器回應字串

    if msg == "Hi":
        reply = "Hello!"  # 將字串"Hello!"指定給reply變數(socket只能傳送字元)
        client.send(
            reply.encode("utf8")
        )  # 傳送回應訊息給客戶端(將字串編碼為utf8格式) 這和 client.send(b"Hello!") 是一樣的
    elif msg == "Bye":
        client.send(b"quit")  # 傳送結束訊息給客戶端(以位元組格式傳送)
        break  # 跳出迴圈，結束程式
    else:
        reply = "What?"  # 將字串"What?"指定給reply變數(socket只能傳送字元)
        client.send(reply.encode("utf8"))  # 傳送回應訊息給客戶端(將字串編碼為utf8格式)

client.close()  # 關閉與客戶端的連線
server_socket.close()  # 關閉伺服器(伺服器端Socket物件)
