import network
import time
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c)

ap = network.WLAN(network.AP_IF)
ap.active(False)
time.sleep(1)
ap.active(True)
ap.config(ssid='FreeWiFi', security=0) # change the AP name that you want
ap.ifconfig(('192.168.1.1', '255.255.255.0', '192.168.1.1', '192.168.1.2'))

oled.fill(0)
oled.text("WiFi Pineapple", 0, 0)
oled.text("AP: FreeWiFi", 0, 20) # change the AP name you want here for display on the oled
oled.text("IP: 192.168.1.1", 0, 40)
oled.show()

# this will keep the AP active
while True:
    oled.fill(0)
    oled.text("WiFi Pineapple", 0, 0)
    oled.text("AP: FreeWiFi", 0, 20)
    if ap.active():
        client_count = len(ap.status('stations'))
        oled.text("Status: Active", 0, 40)
        oled.text(f"Clients: {client_count}", 0, 50)
    else:
        oled.text("Status: Inactive", 0, 40)
    oled.show()
    time.sleep(2)
