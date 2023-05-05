import helpers
import urequests as requests
from utime import sleep
import network
from machine import Pin, PWM
import machine
import sensors

wlan = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

#Motor
in2 = PWM(Pin(26))     # Speed
in1 = Pin(27, Pin.OUT)  # Direction
in1.off()
in2.duty(0)


#Buzzer
buzzer = Pin(17, Pin.OUT)
buzzer.value(0)

#Button
button = Pin(21,Pin.IN,  Pin.PULL_UP)


        
setting = helpers.open_file("device_settings.json")       
      

class Device:
    def __init__(self, settings):
        self.settings = settings
        self.secret = settings["device_secret"]
        self.portion = settings["device_settings"]["portion"]
        self.sound = settings["device_settings"]["sound"]
    
    
    def manuel_feed(self, portion, sound):
        sensors.move(portion, sound)
    
    def feed(self):
        sensors.move(self.portion, self.sound)
        
    def connect_wifi(self, ssid, password):
        helpers.connect_router(ssid, password)
        
    def wifi_reconnect(self, ssid, password):
        helpers.wifi_reconnect(ssid, password)
        
    def has_internet_connection(self):
        try:
            for x in range (15):
                test_connection = requests.get("http://clients3.google.com/generate_204")
                response = test_connection.status_code
                if response == 204:
                    return True
                else:
                    print(f"No internet connection. will try to check again {x}...")
                    sleep(10) 
            
        except Exception as e:
            print(e)
            return False
    
    def scan_wifi(self):
        wifi_list = helpers.scan_wifi()
        return wifi_list
    
        
        
 

dev = Device(setting)



a = dev.has_internet_connection()
print(a)

        