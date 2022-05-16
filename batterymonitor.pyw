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

# Checks battery's current percent each second
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

        # Updating tray icon's tooltip
        sysTrayIcon.update(hover_text = ("Cargando: " if charging else "Descargando: ") + f'{battery.percent}%')

        if(charging and not battery.power_plugged): # If battery must be connected...
            plug(True)
        elif(not charging and battery.power_plugged): #If battery must be disconnected...
            plug(False)

        sleep(1000)

# Custom sleep function, to sleep only if battery monitor is running
def sleep(miliseconds):
    start_time = round(time() * 1000)
    while(running and round(time() * 1000) - start_time < miliseconds):
        pass

# Set plug state
def plug(on):
    # Triying to make a GET request...
    url = on_url if on else off_url
    if(url):
        response = get(url)
        if(response):
            if(response[0] == 200):
                sleep(6000)
                battery = sensors_battery()
                if(on and battery.power_plugged or not on and not battery.power_plugged):
                    return
    
    if(on): # Double beep if battery must be connected
        Beep(655, 250)
        Beep(655, 300)
    else:
        Beep(655, 550) # Single long beep if battery must be disconnected

    sleep(5000)

# Perform a GET request and return response data as a tuple
def get(url):
    try:
        with urlopen(Request(url), timeout = 10) as response:
            return (response.status, response.read().decode())
    except: return None

# Write current charging status into registry and update tray icon's text
def set_charging_status(new_charging_status):
    global charging
    charging = new_charging_status
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_subkey) as new_key:
        winreg.SetValueEx(new_key, reg_value, 0, winreg.REG_DWORD, charging)

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
min_percent = int(config['BATTERY_RANGE']['min_percent'])
max_percent = int(config['BATTERY_RANGE']['max_percent'])
locals().update(config['REG'])
locals().update(config['URLS'])

load_charging_status()

# Checking if there is a file path as an argument, if so have it open when this script is closed
caller = None
if len(argv) > 1:
    if path.exists(argv[1]):
        caller = path.realpath(argv[1])

# Creating tray icon
<<<<<<< HEAD
charging_tray_text = f"Charging to {max_percent}%"
discharging_tray_text = f"Discharging to {min_percent}%"
=======
>>>>>>> 1315ff2 (Version 2.2.0)
menu_options = (
    (f"Ping to {ping_domain}", None, lambda systray: system(f'ping {ping_domain} & TIMEOUT /T 6')),
    ("Open script folder", None, lambda systray: startfile(scr_path))
)
sysTrayIcon = SysTrayIcon(scr_path + "\plug.ico", f"Cargando al {max_percent}%" if charging else f"Descargando al {min_percent}%", menu_options, on_quit = on_closing, default_menu_index = 0)
sysTrayIcon.start()

# Start battery monitor
start()