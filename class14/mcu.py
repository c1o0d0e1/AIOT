class gpio:
    def __init__(self):
        self._D0 = 16
        self._D1 = 5
        self._D2 = 4
        self._D3 = 0
        self._D4 = 2
        self._D5 = 14
        self._D6 = 12
        self._D7 = 13
        self._D8 = 15
        self._SDD3 = 10
        self._SDD2 = 9

    @property
    def D0(self):
        return self._D0

    @property
    def D1(self):
        return self._D1

    @property
    def D2(self):
        return self._D2

    @property
    def D3(self):
        return self._D3

    @property
    def D4(self):
        return self._D4

    @property
    def D5(self):
        return self._D5

    @property
    def D6(self):
        return self._D6

    @property
    def D7(self):
        return self._D7

    @property
    def D8(self):
        return self._D8

    @property
    def SDD3(self):
        return self._SDD3

    @property
    def SDD2(self):
        return self._SDD2


import network


class wifi:
    def __init__(self, ssid=None, password=None):
        """
        初始化 WiFi 物件(模組)
        ssid: WiFi 名稱
        password: WiFi 密碼
        """
        self.sta = network.WLAN(
            network.STA_IF
        )  # 建立 WLAN 物件，設定為站台模式 (初始化 STA 模式)
        self.ap = network.WLAN(
            network.AP_IF
        )  # 建立 WLAN 物件，設定為存取點模式 (初始化 AP 模式)
        self.ssid = ssid  # WiFi 名稱
        self.password = password  # WiFi 密碼
        self.ap.active(False)  # 關閉存取點模式
        self.sta.active(False)  # 關閉站台模式
        self.ip = None  # IP 位址(電腦位址)

    def setup(self, ap_active=False, sta_active=False):
        """
        設定 WiFi 模組的工作模式
        ap_active: 是否啟用存取點模式 (預設: False)
        sta_active: 是否啟用站台模式 (預設: False)

        使用方法:
        wi.setup(ap_active=True|False, sta_active=True|False)
        """
        self.ap_active = ap_active  # 將區域變數 ap_active 指定給方法 ap_active
        self.sta_active = sta_active  # 將區域變數 sta_active 指定給方法 sta_active
        self.ap.active(ap_active)  # 設定存取點模式
        self.sta.active(sta_active)  # 設定站台模式

    def scan(self):
        """
        搜尋附近的無線網路 (搜尋 wi-fi 熱點)
        回傳: 搜尋到的無線網路列表(wifi 列表)

        使用方法:
        wi.scan()
        """
        if self.sta_active:
            wifi_list = self.sta.scan()  # 搜尋附近的無線網路 (搜尋 AP)
            print("Scan results: ")
            for i in range(len(wifi_list)):
                print(wifi_list[i][0])
        else:
            print("STA 模式未啟用，無法搜尋無線網路。")

    def connect(self, ssid=None, password=None) -> bool:
        """
        連接到指定的無線網路
        ssid: WiFi 名稱
        password: WiFi 密碼
        回傳: 連接是否成功 (True/False)

        使用方法:
        wi.connect("WiFi_NAME", "WiFi_PASSWORD")
        或在初始化時有設定過就可以不再設定
        wi.connect()
        """
        ssid = ssid if ssid is not None else self.ssid
        password = password if password is not None else self.password
        if not self.sta_active:
            print("STA 模式未啟用，無法連接無線網路。")
            return False

        if ssid is None or password is None:
            print("wifi 名稱或密碼未設定。")
            return False

        if self.sta_active:
            self.sta.connect(ssid, password)  # 連接到指定的無線網路
            while not (self.sta.isconnected()):  # 等待連接成功
                pass
            self.ip = self.sta.ifconfig()[0]  # 取得 IP 位址
            print(
                "connet successfully", self.sta.ifconfig()
            )  # 顯示網路設定(顯示連接成功的 IP 位址)
            return True


import sys
from machine import Pin, PWM
from umqtt.simple import MQTTClient


class LED:
    def __init__(self, r_pin, g_pin, b_pin, pwm: bool = False):
        """
        LED 類別用於控制 RGB LED 燈

        屬性:
            RRD (pin): 紅色 LED 腳位
            GREEN (pin): 綠色 LED 腳位
            BLUE (pin): 藍色 LED 腳位

        方法:
            __init__(r_pin, g_pin, b_pin, pwm=False): 初始化 LED 物件
            當 pwm=False 時，使用 Pin 類別控制 LED
            當 pwm=True 時，使用 PWM 類別控制 LED
            RED.value(0 or 1): 設定紅色 LED 亮度 (0: 關閉, 1: 開啟)
            GREEN.value(0 or 1): 設定綠色 LED 亮度 (0: 關閉, 1: 開啟)
            BLUE.value(0 or 1): 設定藍色 LED 亮度 (0: 關閉, 1: 開啟)
            RED.duty(duty): 設定紅色 LED PWM 佔空比 (0-1023)
            GREEN.duty(duty): 設定綠色 LED PWM 佔空比 (0-1023)
            BLUE.duty(duty): 設定藍色 LED PWM 佔空比 (0-1023)
        """
        self.pwm = pwm
        if pwm == False:
            self.RED = Pin(r_pin, Pin.OUT)
            self.GREEN = Pin(g_pin, Pin.OUT)
            self.BLUE = Pin(b_pin, Pin.OUT)
        else:
            frequency = 1000  # PWM 頻率設為 1000Hz
            duty_cycle = 0  # PWM 初始佔空比設為 0 (關閉 LED)
            self.RED = PWM(Pin(r_pin), freq=frequency, duty=duty_cycle)
            self.GREEN = PWM(Pin(g_pin), freq=frequency, duty=duty_cycle)
            self.BLUE = PWM(Pin(b_pin), freq=frequency, duty=duty_cycle)

    def LED_open(self, RED_value, GREEN_value, BLUE_value):
        """
        LED_open 開啟方法
        LED_open(RED_value, GREEN_value, BLUE_value)
        例如:
        led = LED(r_pin=5, g_pin=4, b_pin=0, pwm=False)
        led.LED_open(1, 0, 0) # 紅色

        led= LED(r_pin=5, g_pin=4, b_pin=0, pwm=True)
        led.LED_open(512, 0, 0) # 紅色 (PWM 半亮)
        """

        if self.pwm == False:
            self.RED.value(RED_value)
            self.GREEN.value(GREEN_value)
            self.BLUE.value(BLUE_value)
        else:
            self.RED.duty(RED_value)
            self.GREEN.duty(GREEN_value)
            self.BLUE.duty(BLUE_value)


class MQTT:
    def __init__(self, client_id, server, user, password, keepalive):
        """
        初始化 MQTT 物件
        client_id: MQTT 客戶端 ID
        server: MQTT 伺服器位址
        user: 使用者名稱 (可選)
        password: 密碼 (可選)
        keepalive: 保持連線時間
        """
        self.client_id = client_id
        self.server = server
        self.user = user
        self.password = password
        self.keepalive = keepalive
        self.mqClient = MQTTClient(
            self.client_id,
            self.server,
            user=self.user,
            password=self.password,
            keepalive=self.keepalive,
        )

    def connect(self):
        """
        連接到 MQTT 伺服器
        失敗時結束程序
        """
        try:
            self.mqClient.connect()
        except:
            sys.exit()
        finally:
            print("Connected MQTT server")

    def subscribe(self, topic: str, callback: function):
        """
        訂閱主題並設置回條函數
        topic: 要訂閱的MQTT主題
        callback(function): 收到訊息時的回呼函式
        """
        self.mqClient.set_callback(callback)
        self.mqClient.subscribe(topic)

    def check_msg(self):
        """
        檢查是否有訂閱主題發布的資料
        等待已訂閱的主題發送資料
        持續保持連線
        """
        self.mqClient.check_msg()

    def publish(self, topic: str, msg: str):
        topic = topic.encode("utf-8")
        msg = msg.encode("utf-8")
        self.mqClient.publish(topic, msg)


from machine import UART


class MP3:
    def __init__(self):
        """
        初始化 MP3 播放器的基本属性(如音量、播放狀態等)。
        這個方法設置了 MP3 播放器的初始狀態。
        使用 UART1,鮑率 9600

        使用方法:
            mp3 = MP3()
        """
        self.uart = UART(1, baudrate=9600)
        self.uart.init(9600, bits=8, parity=None, stop=1)

    def start(self, volume=100, song=1):
        """
        播放指定歌曲

        volume(int): 音量大小 (0~127), 預設值為 100 (0x64)
        song(int): 歌曲編號 (1~16), 預設值為 1 (0x01)

        使用方法:
        mp3.start(volume=0x64, song=0x01)
        """
        volume = int(hex(volume), 16)
        song = int(hex(song), 16)
        # Volume control (13)
        # Command: AA 13 01 VOL SM
        buf1 = bytearray(5)
        buf1[0] = 0xAA
        buf1[1] = 0x13
        buf1[2] = 0x01
        buf1[3] = volume
        buf1[4] = buf1[0] + buf1[1] + buf1[2] + buf1[3]
        self.uart.write(buf1)

        # Specify song (07)
        # Command: AA 07 02 filename(hi) filename(Lw) SONG SM
        but = bytearray(6)
        but[0] = 0xAA
        but[1] = 0x07
        but[2] = 0x02
        but[3] = 0x00  # 音樂檔案開頭名稱的16進制
        but[4] = song  # 音樂檔案結尾名稱的16進制
        but[5] = but[0] + but[1] + but[2] + but[3] + but[4]
        self.uart.write(but)

    def stop(self):
        """
        停止播放音樂

        使用方法:
            mp3.stop()
        """
        # Stop (04)
        # Command: AA 04 00 AE
        buf = bytearray(4)
        buf[0] = 0xAA
        buf[1] = 0x04
        buf[2] = 0x00
        buf[3] = 0xAE
        self.uart.write(buf)
