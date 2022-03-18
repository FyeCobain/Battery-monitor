from os import path, startfile
from re import sub
from sys import argv
from time import time
from urllib.request import urlopen, Request
import winreg
from winsound import Beep
from infi.systray import SysTrayIcon
from psutil import sensors_battery
from ruamel.yaml import YAML

# Current charging status
charging = False

# Checks battery's current percent each 0.5 seconds
running = True
def start():
    global running
    global charging
    while(running):
        # Getting battery info
        battery = sensors_battery()

        if(battery.percent < minPercent): # If min percent reached...
            sysTrayIcon.update(hover_text = chargingTrayText)
            setChargingStatus(True)
        elif(battery.percent > maxPercent): # If max percent reached...
            sysTrayIcon.update(hover_text = dischargingTrayText)
            setChargingStatus(False)

        if(charging and not battery.power_plugged): # If battery must be connected...
            connect(battery.percent)
        elif(not charging and battery.power_plugged): #If battery must be disconnected...
            disconnect(battery.percent)
        
        sleep(500)

# Custom sleep function, to sleep only if battery monitor is running
def sleep(miliseconds):
    startTime = round(time() * 1000)
    while(running and round(time() * 1000) - startTime < miliseconds):
        pass

# When the battery must be connected...
def connect(batteryPercent):
    # Triying to make GET request
    if(onURL):
        response = GET(onURL)
        if(response):
            if(response[0] == 200):
                if(running):
                    sleep(5000)
                return
    # Play a sound for "low battery"
    Beep(655, 250)
    Beep(655, 300)
    if(running):
        sleep(5000)

# When the battery must be disconnected...
def disconnect(batteryPercent):
    # Triying to make GET request
    if(offURL):
        response = GET(offURL)
        if(response):
            if(response[0] == 200):
                if(running):
                    sleep(5000)
                return
    # Play a sound for "battery too charged"
    Beep(655, 550)
    if(running):
        sleep(5000)

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

# When closing, stop battery monitor and run "caller" file (if not None)
def on_closing(sysTrayIcon):
    global running
    running = False
    if(caller):
        startfile(caller)

# Getting current script path
scrPath = sub(r'\\[^\\]*$', '', path.realpath(__file__))

# Getting config as variables from the "config.yaml" file
configFile = scrPath + '\config.yaml'
yaml = YAML()
with open(configFile) as file:
    config = yaml.load(file)
    locals().update(config)
    loadChargingStatus()

# Checking if there is a file path as an argument, if so have it open when this script is closed
caller = None
if len(argv) > 1:
    if path.exists(argv[1]):
        caller = path.realpath(argv[1])

# Creating tray icon
chargingTrayText = f"Charging to {maxPercent}%"
dischargingTrayText = f"Discharging to {minPercent}%"
menu_options = (("Open script folder", None, lambda systray: startfile(scrPath)),)
sysTrayIcon = SysTrayIcon(scrPath + "\plug.ico", chargingTrayText if charging else dischargingTrayText, menu_options, on_quit = on_closing, default_menu_index = 0)
sysTrayIcon.start()

# Start battery monitor
start()