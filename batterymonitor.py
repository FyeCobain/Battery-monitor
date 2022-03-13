from os import path, system
from re import sub
from sys import argv
from time import sleep
from urllib.request import urlopen, Request
import winreg
from psutil import sensors_battery
from ruamel.yaml import YAML
system('cls')

#Current charging status
charging = False

#Checks battery's current percent each 0.5 sec
running = True
def start():
    global running
    global charging
    while(running):
        #Getting battery info
        battery = sensors_battery()

        if(battery.percent < minPercent): #If min percent reached...
            setChargingStatus(True)
        elif(battery.percent > maxPercent): #If max percent reached...
            setChargingStatus(False)

        if(charging and not battery.power_plugged): #If battery must be connected...
            connect()
        elif(not charging and battery.power_plugged): #If battery must be disconnected...                plugOff()
            disconnect()
        else:
            print(charging, battery.percent)
        
        sleep(1.05)

#When the battery must be connected...
def connect():
    if(onURL):
        print(GET(onURL))
        sleep(5)
    else:
        print('Please connect your battery...')
        sleep(10)

#When the battery must be disconnected...
def disconnect():
    if(offURL):
        print(GET(offURL))
        sleep(5)
    else:
        print('Please disconnect your battery...')
        sleep(10)

#Write current charging status into registry
def setChargingStatus(newChargingStatus):
    global charging
    charging = newChargingStatus
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, regKeyName) as newKey:
        winreg.SetValueEx(newKey, regValueName, 0, winreg.REG_DWORD, charging)

#Read current charging status from registry
def loadChargingStatus():
    global charging
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, regKeyName, 0, winreg.KEY_ALL_ACCESS) as key:
            charging = winreg.QueryValueEx(key, regValueName)[0]
    except:
        setChargingStatus(charging)

#Perform a GET request and return response data as a tuple
def GET(url):
    try:
        with urlopen(Request(url)) as response:
            return (response.status, response.read().decode())
    except: return None

#Getting current config as variables from the "config.yaml" file
configFile = sub('\\\\[^\\\\]*$', '', path.realpath(__file__)) + '\config.yaml'
yaml = YAML()
with open(configFile) as file:
    config = yaml.load(file)
    locals().update(config)
    loadChargingStatus()

#Checking if there is a file path as an argument, if so have it open when this script is closed
caller = None
callerPath = None
if len(argv) > 1:
    if path.exists(argv[1]):
        caller = path.realpath(argv[1])
        callerPath = sub('\\\\[^\\\\]*$', '', caller)

#Start battery monitor
start()