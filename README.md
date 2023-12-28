# RPI-BOT

Telegram bot control of Raspberry Pi

![alt text](https://github.com/Py4Rpi/RPI-BOT/blob/master/screen.jpg)

## Description


This is my pet project/diploma work at Python Developer course. It is a simple Telegram bot which aims to control a Raspberry Pi 4 with LTE modem.
In this case Telegram server works as a middle point between two devices with mobile internet (LTE) and connects them even thou they have a dynamic IP.
My Raspberry Pi 4 setup includes Waveshare SIM7600E-H 4G modem HAT and Sequent Microsystems 8-relay HAT.  

## Getting Started

### Dependencies

I use Ubuntu 20.10 on my Rpi and Python 3.7.

Use requirements.txt to install:

* pytelegrambotapi>=3.7.6
* paramiko>=2.7.1
* gpiozero>=1.5.1
* lib8relay>=1.0.3
* smbus>=1.1.post2

### Installing

To install the bot you can just download it as a ZIP file or use "gh repo clone Py4Rpi/RPI-BOT" command. 
Then just copy the code in your home dir and setup config.py with your own credentials. You will have to 
register your own telegram bot and get the token from Bot Father.

### Executing program

* When dependencies and installing steps are completed you can just open terminal, go to dir with bot and run it :

```
python3 rpibot.py
```

If all goes well it will send the initial message that "RPI BOT ONLINE" as well as current IP of your Raspberry.

The Rpi-bot will give you some options to navigate in menu. There are 3 features so far: 

* relay control 
* terminal access(Paramiko)
* some commands execution(Subprocess)

## Help

Keep in mind that it is just a simple pet project and there are no any warranty that it will work on your setup.

If any troubles you can use Issue Tracker to notify me.
