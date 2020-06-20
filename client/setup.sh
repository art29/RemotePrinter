#!/bin/sh
# setup.sh
(crontab -l 2>/dev/null || true; echo "@reboot sh /home/pi/client/ngrokLauncher.sh >/home/pi/client/logs/cronlog 2>&1") | crontab -
(crontab -l 2>/dev/null || true; echo "@reboot sh /home/pi/client/appLauncher.sh >/home/pi/client/logs/cronlog 2>&1") | crontab -
