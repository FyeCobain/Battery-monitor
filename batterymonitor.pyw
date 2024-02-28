import subprocess
from os import path, system, startfile
from re import search, sub
from sys import argv
from time import time
from configparser import ConfigParser
from urllib.request import urlopen, Request
import winreg
from winsound import Beep
from infi.systray import SysTrayIcon

# Current charging status
charging = True

# Startup info for subprocesses
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Checks battery's current percent each second
running = True
def start():
    global running
    global charging
    while running:
        # Getting battery info
        battery_percent = get_battery_percent()

        if battery_percent <= min_percent: # If min percent reached...
            set_charging_status(True)
        elif battery_percent >= max_percent: # If max percent reached...
            set_charging_status(False)

        # Getting charging status
        load_charging_status()

        # Updating tray icon's tooltip
        sysTrayIcon.update(hover_text = ("Charging" if charging else "Discharging") + f': {battery_percent}%')

        charger_plugged = charger_is_plugged()
        if charging and not charger_plugged: # If battery must be connected...
            plug(True)
        elif not charging and charger_plugged: #If battery must be disconnected...
            plug(False)

        sleep(1500)

# Returns the current battery percent
def get_battery_percent():
    process = subprocess.Popen('WMIC PATH Win32_Battery Get EstimatedChargeRemaining', startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return int(search("\d+", str(process.stdout.read())).group(0))

# Returns true if the charger is plugged in
def charger_is_plugged():
    process = subprocess.Popen('WMIC Path Win32_Battery Get BatteryStatus', startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return (search("\d+", str(process.stdout.read())).group(0)) == '2'

# Custom sleep function, to sleep only if battery monitor is running
def sleep(miliseconds):
    start_time = round(time() * 1000)
    while running and round(time() * 1000) - start_time < miliseconds:
        continue

# Set plug state
def plug(on):
    sleepTime = 5000
    # Performing a GET request
    url = on_url if on else off_url
    if url:
        response = get(url)
        if response:
            if response[0] == 200:
                sleep(sleepTime * 2)
                sleepTime = 0
                charger_plugged = charger_is_plugged()
                if on and charger_plugged or not on and not charger_plugged:
                    return
    # Executing the "Smart Plug Switch" script
    elif path.isfile(switch_path) and d_id and d_ip and d_key and d_protocol:
        state = 'ON' if on else 'OFF'
        process = subprocess.Popen(f'python "{switch_path}" "{d_id}" "{d_ip}" "{d_key}" "{d_protocol}" {state}', startupinfo=startupinfo)
        process.wait()
        sleep(sleepTime)
        sleepTime = 0
        charger_plugged = charger_is_plugged()
        if on and charger_plugged or not on and not charger_plugged:
            return
    
    if on: # Double beep if battery must be connected
        Beep(655, 200)
        sleep(25)
        Beep(655, 300)
    else:
        Beep(655, 550) # Single long beep if battery must be disconnected

    sleep(sleepTime)

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
    global caller
    running = False
    if caller:
        startfile(caller)
        caller = None
        
# Getting current script path
scr_path = sub(r'\\[^\\]*$', '', path.realpath(__file__))
# Smart Switch Plug script path
switch_path = f'{scr_path}\\smart_plug_switch.py'

# Getting config as variables from the "config.ini" file
config = ConfigParser()
config.read(scr_path + '\config.ini')
min_percent = int(config['BATTERY_RANGE']['min_percent'])
max_percent = int(config['BATTERY_RANGE']['max_percent'])
locals().update(config['REG'])
locals().update(config['URLS'])
locals().update(config['PLUG_DEVICE'])

load_charging_status()

# Checking if there is a file path as an argument, if so have it open when this script is closed
caller = None
if len(argv) > 1:
    if path.exists(argv[1]):
        caller = path.realpath(argv[1])

# Creating tray icon
if ping_domain:
    menu_options = (
        (f"Ping to {ping_domain}", None, lambda systray: system(f'ping {ping_domain} & TIMEOUT /T 6')),
        ("Open script dir", None, lambda systray: startfile(scr_path))
    )
else:
    menu_options = (
        ("Open script dir", None, lambda systray: startfile(scr_path)),
    )

sysTrayIcon = SysTrayIcon(scr_path + "\plug.ico", f"Charging to {max_percent}%" if charging else f"Discharging to {min_percent}%", menu_options, on_quit = on_closing, default_menu_index = 0)
sysTrayIcon.start()

# Start battery monitor
start()