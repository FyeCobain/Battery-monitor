from os import path, system
from re import sub
import subprocess, shlex
from sys import argv
from time import sleep, time
from tkinter import Tk
from urllib.request import urlopen, Request
import winreg
from winsound import Beep
from psutil import sensors_battery
from ruamel.yaml import YAML

# Current charging status
charging = False

# Checks battery's current percent each 0.5 sec
running = True
def start():
    global running
    global charging
    while(running):
        # Getting battery info
        battery = sensors_battery()

        if(battery.percent < minPercent): # If min percent reached...
            setChargingStatus(True)
        elif(battery.percent > maxPercent): # If max percent reached...
            setChargingStatus(False)

        if(charging and not battery.power_plugged): # If battery must be connected...
            connect(battery.percent)
        elif(not charging and battery.power_plugged): #If battery must be disconnected...                plugOff()
            disconnect(battery.percent)
        
        sleep(0.5)

# When the battery must be connected...
def connect(batteryPercent):
    # Triying to make GET request
    if(onURL):
        response = GET(onURL)
        if(response):
            if(response[0] == 200):
                sleep(5)
                return

    # Play a sound for "low battery"
    Beep(655, 250)
    Beep(655, 300)
    sleep(5)

# When the battery must be disconnected...
def disconnect(batteryPercent):
    # Triying to make GET request
    if(offURL):
        response = GET(offURL)
        if(response):
            if(response[0] == 200):
                sleep(5)
                return

    # Play a sound for "battery too charged"
    Beep(655, 550)
    sleep(5)

# Write current charging status into registry
def setChargingStatus(newChargingStatus):
    global charging
    charging = newChargingStatus
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, regSubKeyName) as newKey:
        winreg.SetValueEx(newKey, regValueName, 0, winreg.REG_DWORD, charging)

# Read current charging status from registry
def loadChargingStatus():
    global charging
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, regSubKeyName, 0, winreg.KEY_ALL_ACCESS) as key:
            charging = winreg.QueryValueEx(key, regValueName)[0]
    except:
        setChargingStatus(charging)

# Perform a GET request and return response data as a tuple
def GET(url):
    try:
        with urlopen(Request(url)) as response:
            return (response.status, response.read().decode())
    except: return None

# Getting current config as variables from the "config.yaml" file
configFile = sub(r'\\[^\\]*$', '', path.realpath(__file__)) + '\config.yaml'
yaml = YAML()
with open(configFile) as file:
    config = yaml.load(file)
    locals().update(config)
    loadChargingStatus()

# Checking if there is a file path as an argument, if so have it open when this script is closed
caller = None
callerPath = None
if len(argv) > 1:
    if path.exists(argv[1]):
        caller = path.realpath(argv[1])
        callerPath = sub(r'\\[^\\]*$', '', caller)

# Start battery monitor
start()