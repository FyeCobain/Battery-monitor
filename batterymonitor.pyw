from os import path, system, startfile
from re import sub
from sys import argv
from time import time
from configparser import ConfigParser
from urllib.request import urlopen, Request
import winreg
from winsound import Beep
from psutil import sensors_battery
from infi.systray import SysTrayIcon

# Current charging status
charging = True

# Checks battery's current percent each 0.5 seconds
running = True
def start():
    global running
    global charging
    while(running):
        # Getting battery info
        battery = sensors_battery()

        if(battery.percent <= min_percent): # If min percent reached...
            set_charging_status(True)
        elif(battery.percent >= max_percent): # If max percent reached...
            set_charging_status(False)

        if(charging and not battery.power_plugged): # If battery must be connected...
            connect(True)
        elif(not charging and battery.power_plugged): #If battery must be disconnected...
            connect(False)
        
        sleep(500)

# Custom sleep function, to sleep only if battery monitor is running
def sleep(miliseconds):
    start_time = round(time() * 1000)
    while(running and round(time() * 1000) - start_time < miliseconds):
        pass

def connect(turn_on):
    # Triying to make a GET request...
    url = on_url if turn_on else off_url
    if(url):
        response = get(url)
        if(response):
            if(response[0] == 200):
                sleep(5000)
                return
    
    if(turn_on): # Double sound if battery must be connected
        Beep(655, 250)
        Beep(655, 300)
    else:
        Beep(655, 550) # Single sound if battery must be disconnected

    sleep(5000)

# Perform a GET request and return response data as a tuple
def get(url):
    try:
        with urlopen(Request(url)) as response:
            return (response.status, response.read().decode())
    except: return None

# Write current charging status into registry and update tray icon's text
def set_charging_status(new_charging_status):
    global charging
    charging = new_charging_status
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_subkey) as new_key:
        winreg.SetValueEx(new_key, reg_value, 0, winreg.REG_DWORD, charging)
    try:
        sysTrayIcon.update(hover_text = charging_tray_text if charging else discharging_tray_text)
    except:
        pass

# Read current charging status from registry
def load_charging_status():
    global charging
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_subkey, 0, winreg.KEY_ALL_ACCESS) as key:
            charging = winreg.QueryValueEx(key, reg_value)[0]
    except:
        set_charging_status(charging)

# When closing, stop battery monitor and run "caller" file (if not None)
def on_closing(sysTrayIcon):
    global running
    running = False
    if(caller):
        startfile(caller)
        
# Getting current script path
scr_path = sub(r'\\[^\\]*$', '', path.realpath(__file__))

# Getting config as variables from the "config.ini" file
config = ConfigParser()
config.read(scr_path + '\config.ini')
locals().update(config['BATTERY_RANGE'])
locals().update(config['REG'])
locals().update(config['URLS'])
min_percent = int(min_percent)
max_percent = int(max_percent)

load_charging_status()

# Checking if there is a file path as an argument, if so have it open when this script is closed
caller = None
if len(argv) > 1:
    if path.exists(argv[1]):
        caller = path.realpath(argv[1])

# Creating tray icon
charging_tray_text = f"Charging to {max_percent}%"
discharging_tray_text = f"Discharging to {min_percent}%"
menu_options = (
    (f"Ping to {ping_domain}", None, lambda systray: system(f'ping {ping_domain} & TIMEOUT /T 6')),
    ("Open script folder", None, lambda systray: startfile(scr_path))
)
sysTrayIcon = SysTrayIcon(scr_path + "\plug.ico", charging_tray_text if charging else discharging_tray_text, menu_options, on_quit = on_closing, default_menu_index = 0)
sysTrayIcon.start()

# Start battery monitor
start()