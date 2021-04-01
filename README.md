# RemotePrinter

Remote Printer is an add-on for your 3D Printer, using [OctoPrint](https://octoprint.org/) to control your printer with your voice using the Google Assistant. This is part of a group of projects that are were created over time, which is called ![](OctoRGB_Logo_Orange.svg).

## Deprication
The code that is in this repo only works with Dialogflow old's version which is now depricated, it will still work but is not actually supported anymore by google. I will try to upgrade to new ways of doing it in the next few months.

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

**For the server part, make sure you have a Python 3 server with all needed dependencies installed and a domain. I use [Phusion Passenger](https://www.phusionpassenger.com/library/walkthroughs/start/python.html) with Apache, but you can use what suits you better !**

*You also need to make sure that you got a copy of the DialogFlow app to be able to use the server part, you can setup the DialogFlow app using the zip and importing it, you then need to configure Actions on Google, if you need help send me a message !*
1) Copy the server folder to your desired location on your server
2) Configure the Python server (If you are not sure how to do that, Digital Ocean have great tutorials)
3) Install all necessary dependencies (Flask, Flask Assistant, Pymysql, Jose, Requests ...)
4) Rename the sample_conf.py to conf.py
```
mv sample_conf.py conf.py
```
5) Configure the database by modifying the variables in conf.py
```
nano conf.py
```
6) Setup your clients with your own domain
7) Your server should be ready to go ! Restart the server and you can test a client !

## Use
**Right now these are the implemented actions :**

* Get User ID
* Ask for percentage of the print
* Time left on a print
* Temperature of the printer
* Extrude an amount of filament (Ex : "Extrude 50 millimeters")
* Heat Up the printer (Ex : "Change temperature to 200")
* Cool off the printer (Ex : "Change temperature to zero" or "Cool off")
* Home axes (Ex : "Home axes", "Home X axis", "Home X and Z axes")

## Update ideas

* Be able to see the webcam on a phone or Nest Home Hub for example ? (IDK if it's possible)
* Set a reminder when the print will be done ?
* Cancel a print (I don't want to be able to select a print from voice for security measures, someone should always be there to check the print at the beginning)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Questions ?
If you have any questions you can contact me at my pro email : arthur[@]octorgb[.]com

I speak :
- [x] French
- [x] English

You can send me an email in any of these two languages !
