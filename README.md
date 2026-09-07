# Phomemo Cups Driver
Cups driver for Phomemo M02 Pro. Based on the works of other, but tweaked and cleaned up for my setup, which is a raspberry pi zero. See full instructions below.

## Sources
- [Phomemo script](https://github.com/vivier/phomemo-tools/blob/master/tools/phomemo-filter.py)
- [Install cups](https://roundhere.net/field-notes/2025/05/raspberry-pi-print-server/)

## Instructions

### Raspberry pi and cups server
- Get a good power supply for your raspberry pi. If your image starts out printing fast but then slows down, you do not have enough power.
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

- Check for your printer `hcitool scan`
- Test connect `sudo rfcomm connect 0 53:48:0D:83:AA:69`

- Add your user to cups `sudo usermod -a -G lpadmin submarines`
- Configure cups for network access `sudo nano /etc/cups/cupsd.conf`
```conf
    
    # Change "Listen localhost:631" to "Port 631"
    Listen localhost:631
    Port 631

    # Add retry interval (optional, default is 30)
    JobRetryInterval 10

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

- Restart cups `sudo /etc/init.d/cups restart`

- Auto connect cups to network after reboot `sudo nano /etc/network/if-up.d/cups`
```shell
#!/bin/sh
sudo systemctl restart cups.service
```
- Make executable `sudo chmod +x /etc/network/if-up.d/cups`

### Cups driver
- Build cups drivers
```shell
make
sudo make install
```

- Install drivers
```shell

# To add
sudo lpadmin -p M02 -E -v phomemo://53480D83AA69  -P /usr/share/cups/model/phomemo/phomemo-m02pro.ppd.gz -o printer-error-policy=retry-job

# To remove
sudo lpadmin -x M02
```

If all went well, the printer should now appear on all your apple devices. If you change the `cups/backend/phomemo.py` file to suit your setup, re-running make+sudo make install is enough to run your new code. For cups error logs: `tail /var/log/cups/error_log -f` - they are not the best.
