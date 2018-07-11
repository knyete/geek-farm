"Utils"

from geek_farm import models
from geek_farm import config

def disconnect():
    if platform() == "linux":
        return True
    import network
    nic = network.WLAN(network.STA_IF)
    if not nic.active():
        led(config.L_ST_WIFI, False)
        return True
    if nic.isconnected():
        nic.disconnect()
        led(config.L_ST_WIFI, False)
    return True
    
def led(pin, on=True):
    """led."""
    if platform() == "linux":
        return True
    import machine
    led = machine.Pin(pin, machine.Pin.OUT)
    if on:
        led.off()
        return on
    else:
        led.on()
        return on

def get_time():
    """Return localtime."""
    config.LOG.info("utils:Get current time.")
    if platform() == "linux":
        return get_time_linux()
    elif platform() == "esp8266":
        return get_time_esp()
    else:
        return False

def get_time_linux():
    """Get time linux."""
    import utime
    return utime.mktime(utime.localtime())

def get_time_esp():
    """Get time esp8266."""
    import utime
    return utime.mktime(utime.localtime())

def connect_wifi(ssid, key):
    """Connect Wifi."""
    config.LOG.info("utils:Connecting to: %s" % ssid)
    if platform() == "linux":
        return connect_wifi_linux(ssid, key)
    elif platform() == "esp8266":
        return connect_wifi_esp(ssid, key)
    else:
        return False

def connect_wifi_linux(ssid, key):
    """Connect wifi linux."""
    led(config.L_ST_WIFI, True)
    return True

def connect_wifi_esp(ssid, key):
    """Connect wifi esp8266."""
    import network
    import utime
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    nic.connect(ssid, key)
    start = get_time()
    while not nic.isconnected():
        # wait 1sec
        utime.sleep(1)
        now = get_time()
        if now > start+30:
            break
    if nic.isconnected():
        # led on
        config.LOG.info("utils:Connected to: %s" % ssid)
        led(config.L_ST_WIFI, True)
        return True
    else:
        nic.disconnect()
        # led of
        config.LOG.error("utils:Failed connecting to: %s" % ssid)
        led(config.L_ST_WIFI, False)
        return False

def is_first_time():
    """Is first time."""
    config.LOG.debug("utils:Checing if is first time.")
    for data in models.WelcomeModel.scan():
        if data:
            return data
        else:
            return None

def wifi_scan():
    """Wifi scan AP."""
    config.LOG.debug("utils:Scan wifi access points.")
    if platform() == "linux":
        return wifi_scan_linux()
    elif platform() == "esp8266":
        return wifi_scan_esp()
    else:
        return False

def wifi_scan_linux():
    """Wifi scan linux."""
    return [
        {
            "ssid": "teste",
            "channel": "99",
            "signal": "-12",
            "security":  "WPA2-PSK",
            "hidden": "Visible",
        },
        {
            "ssid": "teste-2",
            "channel": "99",
            "signal": "-12",
            "security": "WPA2-PSK",
            "hidden": "Hidden",
        }
    ]

def wifi_scan_esp():
    """Wifi scan AP."""
    import network
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    stations = nic.scan()
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

def get_wifi_info_linux():
    """return wifi info."""
    return {
        'ip': '192.168.0.2',
        'gateway': '192.168.0.1',
        'dns': '8.8.8.8',
        'ssid': 'test',
        'channel': 1
    }

def get_wifi_info_esp():
    """return wifi info."""
    import network
    nic = network.WLAN(network.STA_IF)
    if not nic.active():
        return None
    if nic.isconnected():
        return {
            'ip': nic.ifconfig()[0],
            'gateway': nic.ifconfig()[2],
            'dns': nic.ifconfig()[3],
            'ssid': 'get db',
            'channel': 11
        }
    else:
        return None


def get_wifi_info():
    """return wifi info."""
    config.LOG.info("utils:Getting wifi info.")
    if platform() == "linux":
        return get_wifi_info_linux()
    elif platform() == "esp8266":
        return get_wifi_info_esp()
    else:
        return None

def platform():
    """return platform"""
    config.LOG.debug("utils:Get platform.")
    import sys
    return sys.platform

def version():
    """return version"""
    config.LOG.debug("utils:Get version.")
    return "0.0.1"

def get_info():
    """return informations."""
    config.LOG.info("utils:Get info.")
    return {
        'platform': platform(),
        'version': version(),
        'network': get_wifi_info()
    }