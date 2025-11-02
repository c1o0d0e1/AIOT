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
