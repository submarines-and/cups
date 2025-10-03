# Phomemo Cups Driver
Cups driver for Phomemo M02 Pro. Based on the works of other, but tweaked and cleaned up for my setup.

## Sources
- [Phomemo scripts](https://github.com/vivier/phomemo-tools/blob/master/tools/phomemo-filter.py)
- [Install cups](https://roundhere.net/field-notes/2025/05/raspberry-pi-print-server/)

## Instructions

### Raspberry pi and cups server
- Download [the Raspberry Pi Imager tool](https://www.raspberrypi.com/software/).
- Use it to create a disk image for your pi. I used rpi lite 64bit with no desktop (available on page 2).
- Install dependencies

```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install cups python3 python3-pip python3-devel python-pil3 python3-dbus python3-bluez bluetooth bluez blueman netatalk git
# idk which bluetooth modules are actually necessary. netatalk and git is also just for me

```
- Restart bluetooth
```shell
sudo rfkill unblock bluetooth
sudo systemctl stop bluetooth
sudo systemctl status bluetooth
sudo systemctl restart bluetooth
```

- Add your user to cups `sudo usermod -a -G lpadmin submarines`
- Configure cups for network access `sudo nano /etc/cups/cupsd.conf`
```conf
    
    # Change "Listen localhost:631" to "Port 631"
    Listen localhost:631
    Port 631

    # Add  Allow @local to the following sections
    <Location />
        Order allow,deny
        Allow @local
    </Location>

    <Location /admin>
        Order allow,deny
        Allow @local
    </Location>

    <Location /admin/conf>
        AuthType Default
        Require user @SYSTEM
        Order allow,deny
        Allow @local
    </Location>
``` 

- Restart cups `sudo /etc/init.d/cups restart

- Auto connect cups to network after reboot `sudo nano /etc/network/if-up.d/cups`
```shell
#!/bin/sh
sudo systemctl restart cups.service
```
- Make executable `sudo chmod +x /etc/network/if-up.d/cups`

### Cups driver
- Install cups driver
```shell
cd cups
make
sudo make install
```

If all went well, the printer should now appear on all your apple devices.