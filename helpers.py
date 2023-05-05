import ujson as json
import urequests as requests
from ntptime import settime
import time
import random
import uos
import network, usys
from utime import sleep
import sensors
from time import ticks_ms, ticks_diff

wlan = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

###----- Functions -----###    


# Network

def connect_router(ssid, password):
    wlan.active(False)
    wlan.active(True)
    if wlan.isconnected():
        print("Already Connected.")
        return True
    else:
        wlan.connect(ssid, password)
        start = ticks_ms()
        while not wlan.isconnected():
            if ticks_diff(ticks_ms(), start) > 10_000:
                print("Could not connect")
                return False
        
    
            
def wifi_reconnect(ssid, password):
    if wlan.isconnected():
        return True
    else:
        for x in range(10):   
            connect_router(ssid, password)
            if wlan.isconnected():
                print("Successfuly CONNECTED")
                return True
            else:
                print(f"No wifi connection. Trying to reconnect {x}...")
        print("Could not connected to Wifi with given credentials")   
        return False
        
        
def scan_wifi():
        if not wlan.active():
            wlan.active(True)  
        encoded_list = wlan.scan()
        wifi_list = []
        for i in range (len(encoded_list)):
            decoded = encoded_list[i][0].decode('utf-8')
            wifi_list.append(decoded)  
        list = {"ssid_list": wifi_list}
        return list["ssid_list"]
            


def wlan_disabled():
    wlan_active(False)
    
def ap_disable():
    ap.active(False)
    print("AP Disabled..")
    
def ap_active():
      # set how many clients can connect to the network
    ap.active(True)
    ap.config(essid="ByteFeed", authmode=0)
    
    # set the SSID of the access point
    if ap.active() == True:
        print("AP Active")
        print(ap.ifconfig())
        sensors.buzz(.1)


def randstr():
    source = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join([source[x] for x in [(uos.urandom(1)[0] % len(source)) for _ in range(15)]])

def store_data(fname, data):
    with open(fname, "w+") as f:
            json.dump(data, f)
                 
def open_file(fname):
    with open(fname) as credentials_json:   
        settings = json.loads(credentials_json.read())
        return settings
      
def update_settings(objname, obj):
    settings_file = "device_settings.json"
    a = open_file(settings_file)
    a[objname] = obj
    store_data(settings_file, a)
    
def reset_device():
    default_settings = open_file("default.json")
    store_data('device_settings.json', default_settings)
    
def post_dweet(url, data):
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data)) 
    dweet_back = json.loads(response.content)
    print("Created: ", dweet_back["with"]["created"])
    return dweet_back

def get_dweet(url):
    response = requests.get(url)
    print("Fetching content from ", url, ":")
    latest_dweet = json.loads(response.content)
    dweet = (latest_dweet['with'][0]['content'])
    print(dweet)
    return dweet



    

    