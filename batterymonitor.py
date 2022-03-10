from yaml import load, FullLoader
from psutil import sensors_battery
from time import sleep
from os import system
system('cls')

#Getting current config as variables
with open(r'config.yaml') as file:
    config = load(file, Loader = FullLoader)
locals().update(config)

#Checks battery's current percent each 0.5 sec
def start():
    global charging
    while(True):
        #Getting battery info
        battery = sensors_battery()

        if(battery.percent < minPercent): #If min percent reached...
            charging = True
        elif(battery.percent > maxPercent): #If max percent reached...
            charging = False

        if(charging and not battery.power_plugged): #If battery must be connected...
            plugOn()
        elif(not charging and battery.power_plugged): #If battery must be disconnected...
            plugOff()
        else:
            print('ok')

        #0.5 seconds
        sleep(0.5)

#If battery must be connected...
def plugOn():
    print('plug ON')

#If battery must be disconnected...
def plugOff():
    print('plug OFF')

#Start battery monitor
start()