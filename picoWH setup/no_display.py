import network
import time

ap = network.WLAN(network.AP_IF)
ap.active(False)
time.sleep(1)
ap.active(True)
ap.config(ssid='VlTBPL', security=0) # change the AP name that you want
ap.ifconfig(('192.168.1.1', '255.255.255.0', '192.168.1.1', '192.168.1.2'))

# this will keep the AP active
while True:
    if not ap.active():
        ap.active(True)
