from . import shared
from .models import db
from .models import WifiAPModel
from .models import WifiSTAModel

class Network:
    def __init__(self):
        self.log = shared._log
        self.board = shared._board
        self.db = db
        self.__ip = None
        self.__subnet = None
        self.__gateway = None
        self.__dns = None
        self.__mac = None
    
    @property
    def ip(self):
        return self.__ip
    
    @ip.setter
    def ip(self, value):
        self.__ip = value
    
    @property
    def subnet(self):
        return self.__subnet
    
    @subnet.setter
    def subnet(self, value):
        self.__subnet = value
    
    @property
    def gateway(self):
        return self.__gateway
    
    @gateway.setter
    def gateway(self, value):
        self.__gateway = value
    
    @property
    def dns(self):
        return self.__dns

    @dns.setter
    def dns(self, value):
        self.__dns = value

    @property
    def mac(self):
        return self.__mac
    
    @mac.setter
    def mac(self, value):
        self.__mac = value
    
class WifiAP(Network):
    def __init__(self):
        super().__init__()
        self.log.debug("wifiap: Start constructor")
        self.db.connect()
        row = WifiAPModel.row()
        if not row:
            WifiAPModel.init()
            essid = "%s-%s" % ("geekfarm", self.board.id)
            row = WifiAPModel.save(**{"essid": essid})
            self.log.debug("wifiap: create model")
        for k, v in row.items():
            if k != "created_at":
                setattr(self, k, v)
        self.db.close()
    
    def start(self):
        self.log.info("wifiap: start creating access point")
        if self.board.platform == "esp8266":
            import network
            ap_if = network.WLAN(network.AP_IF)
            if not ap_if.active():
                ap_if.active(True)
            # config ap
            # TODO: mac address
            ap_if.config(channel=self.channel,
                         hidden=self.hidden,
                         authmode=self.authmode,
                         essid=self.essid, 
                         dhcp_hostname=self.hostname,
                         password=self.password)
            ap_if.ifconfig((self.ip, self.mask, self.gateway, self.dns))
            self.log.info("wifiap: esp8266 created access point.")
            return True
        elif self.board.platform == "linux":
            self.log.info("wifiap: linux created access point.")
            return True
        else:
            self.log.error("wifiap: not supported platform.")
            return False
    
    def stop(self):
        self.log.info("wifiap: stoping access point")
        if self.board.platform == "esp8266":
            import network
            ap_if = network.WLAN(network.AP_IF)
            if not ap_if.active():
                self.log.info("wifiap: the access point is already stopped.")
            else:
                ap_if.active(False)
            return True
        elif self.board.platform == "linux":
            self.log.info("wifiap: linux stopping access point.")
            return True
        else:
            self.log.error("wifiap: not supported platform.")
            return False

    def info(self):
        self.db.connect()
        row = WifiAPModel.row()
        self.db.close()
        return row
    
    def save(self):
        self.db.connect()
        row = WifiAPModel.row()
        fields = {k: v for k, v in self.__dict__.items()}
        WifiAPModel.update(row, **fields)
        self.db.close()
        return True

class WifiSTA(Network):
    def __init__(self):
        super().__init__()
        self.log.debug("wifista: Start constructor")
        self.db.connect()
        row = WifiSTAModel.row()
        if row:
            for k, v in row.items():
                if k != "created_at":
                    setattr(self, k, v)
        else:
            self.log.debug("wifista: create table")
        self.db.close()
    
    def connect(self, ssid, key):
        import network
        nic = network.WLAN(network.STA_IF)
        nic.active(True)
        nic.connect(ssid, key)
        import utime
        start = self.board.time
        while not nic.isconnected():
            # wait 1sec
            utime.sleep(1)
            now = self.board.time
            if now > start+30:
                break
        if nic.isconnected():
            self.ip = nic.ifconfig()[0]
            self.mask = nic.ifconfig()[1]
            self.gateway = nic.ifconfig()[2]
            self.dns = nic.ifconfig()[3]
            self.ssid = ssid
            self.password = key
            row = WifiSTAModel.row()
            if row:
                self.update()
            else:
                self.save()
            return True
        else:
            nic.disconnect()
            return False
    
    def disconnect(self):
        import network
        nic = network.WLAN(network.STA_IF)
        nic.disconnect()
        nic.active(False)
        return True
    
    def scan(self):
        import network
        nic = network.WLAN(network.STA_IF)
        nic.active(True)
        stations = nic.scan()
        nic.active(False)
        wifis = [] # stations
        security_types = ['Open','WEP','WPA-PSK','WPA2-PSK','WPA/WPA2-PSK']
        shows = ['Visible','Hidden']
        for w in stations:
            wifi_data = {
                "ssid":    str(w[0], 'utf8'),
                "channel":    str(w[2]),
                "signal":    str(w[3]),
                "security":    security_types[w[4]],
                "hidden":    shows[w[5]],
            }
            wifis.append(wifi_data)
        # sorted by signal
        _aps = sorted(wifis, key=lambda k: (k['ssid'],k['signal']))
        return _aps
    
    def update(self):
        self.db.connect()
        row = WifiSTAModel.row()
        fields = {k: v for k, v in self.__dict__.items()}
        WifiSTAModel.update(row, **fields)
        self.db.close()
        return True

    def save(self):
        self.db.connect()
        row = WifiSTAModel.row()
        if row:
            return row
        else:
            WifiSTAModel.init()    
        fields = {k: v for k, v in self.__dict__.items()}
        row = WifiSTAModel.save(**fields)
        self.db.close()
        return row
    
    def info(self):
        self.db.connect()
        row = WifiSTAModel.row()
        self.db.close()
        return row
