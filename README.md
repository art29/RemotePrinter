# RemotePrinter

Remote Printer is an add-on for your 3D Printer, using [OctoPrint](https://octoprint.org/) to control your printer with your voice using the Google Assistant

## Installation (Client)

**For Remote Printer to work, you need to get access to the alpha/beta of Remote Printer's Assistant App by contacting me by email available down below**

*If you do not have or do not want to configure a server, you can use the default url : https://voice.octorgb.com*

1) Load OctoPrint on your raspberry pi and setup Wifi and SSH (Please see OctoPrint's documentation if you need help doing this)
2) Copy the client folder on your Raspberry Pi
3) Create an account and follow the steps to install [ngrok](https://ngrok.com/) on your Raspberry Pi
4) Run setup.sh to set the CronJobs
```
sh /home/pi/client/setup.sh
```
5) Rename the sample_conf.py to conf.py
```
mv /home/pi/client/sample_conf.py /home/pi/client/conf.py
```
6) Fill the two variables
```
nano /home/pi/client/conf.py
```
(Get the Api Key from OctoPrint's settings and the OAuth ID from asking the Google Assistant "Talk to remote printer" and then "Can I get my user id ?")

7) If using another server than octorgb.com, change the url in client.py
```
nano /home/pi/client/main.py
```
8) Reboot the Raspberry Pi and you should now be good to go ! Don't hesitate to contact me if you have questions or have ideas to make the project better !

## Installation (Server)

In progress
```bash
```

## Usage

In progress
```
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Questions ?
If you have any questions you can contact me at my pro email : arthur[@]octorgb[.]com

I speak :
- [x] French
- [x] English

You can send me an email in any of these two languages !
