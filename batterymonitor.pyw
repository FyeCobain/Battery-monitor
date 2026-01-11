import subprocess
from os import path, system, startfile
from re import search, sub
from sys import argv
from ctypes import windll
from time import time
from configparser import ConfigParser
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json
import winreg
from winsound import PlaySound, SND_FILENAME
from simplesystray import SysTrayIcon
from time import sleep as sl

# Startup info for subprocesses
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Checks battery's current percent each second
running = True
paused = False
kasa_error_codes = []
def start():
    global running
    global paused
    while running:
        if (paused):
            continue

        # Getting battery info
        battery_percent = get_battery_percent()
        charger_plugged = charger_is_plugged()

        # Updating tray icon's tooltip
        sysTrayIcon.update(hover_text = f'{battery_percent}%' + ('' if not charger_plugged else ' (Charging)'))

        if battery_percent <= min_percent and not charger_plugged: # If min percent reached...
            plug(True)
        elif battery_percent >= max_percent and charger_plugged: # If max percent reached...
            plug(False)

        sleep(1500)

# Returns the current battery percent
def get_battery_percent():
    process = subprocess.Popen('WMIC PATH Win32_Battery Get EstimatedChargeRemaining', startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return int(search(r"\d+", str(process.stdout.read())).group(0))

# Returns true if the charger is plugged in
def charger_is_plugged():
    process = subprocess.Popen('WMIC Path Win32_Battery Get BatteryStatus', startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return (search(r"\d+", str(process.stdout.read())).group(0)) == '2'

# Custom sleep function, to sleep only if battery monitor is running
def sleep(miliseconds):
    start_time = round(time() * 1000)
    while running and round(time() * 1000) - start_time < miliseconds:
        continue

# Set plug state
def plug(on, shutingDown = False):
    sleepTime = 5000

    # Performing a GET request
    url = on_url if on else off_url
    if url:
        response = get(url)
        if response:
            if response[0] == 200:
                if not (shutingDown):
                    sleep(sleepTime)
                else:
                    sl(.5)
                sleepTime = 0
                charger_plugged = charger_is_plugged()
                if on and charger_plugged or not on and not charger_plugged:
                    return

    # Performing a POST request
    elif kasa_token and kasa_device_id:
        state = "1" if on else "0"
        response = post(f"https://wap.tplinkcloud.com/?token={kasa_token}", {
            "method": "passthrough",
            "params": {
                "deviceId": kasa_device_id,
                "requestData": "{\"system\":{\"set_relay_state\":{\"state\":" + state + "}}}"
            }
        })
        if response:
            if response[0] == 200:
                if not (shutingDown):
                    sleep(sleepTime)
                else:
                    sl(.5)
                sleepTime = 0
                charger_plugged = charger_is_plugged()
                if on and charger_plugged or not on and not charger_plugged:
                    return

    if on:
        PlaySound(scr_path + r'\sounds\low.wav', SND_FILENAME)
    else:
        PlaySound(scr_path + r'\sounds\hight.wav', SND_FILENAME)

    if not shutingDown:
        sleep(sleepTime)

# Performs a GET request and returns the response data as a tuple
def get(url):
    try:
        with urlopen(Request(url), timeout = 10) as response:
            return (response.status, response.read().decode())
    except:
        return None

# Performs a POST request and returns the response data as a tuple
def post(url, body):
    try:
        request = Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urlopen(request, timeout = 5) as response:
            bodyData = json.loads(response.read().decode("utf-8"))
            error_code = bodyData["error_code"]
            if error_code != 0:
                if not error_code in kasa_error_codes:
                    kasa_error_codes.append(error_code)
                    windll.user32.MessageBoxTimeoutW(0, f"Error { error_code }: { bodyData["msg"] }", "Kasa device error - BatteryMonitor", 0x10, 0, 30000)
            return (response.status, data)
    except Exception as e:
        return None

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

# Getting config as variables from the "config.ini" file
config = ConfigParser()
config.read(scr_path + r'\config.ini')
min_percent = int(config['BATTERY_RANGE']['min_percent'])
max_percent = int(config['BATTERY_RANGE']['max_percent'])
locals().update(config['PING_DOMAIN'])  
locals().update(config['WEBHOOKS'])
locals().update(config['KASA_DEVICE'])

# Returns true if the script will run at start
def does_run_at_start():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS) as key:
            value = winreg.QueryValueEx(key, "BatteryMonitor")[0]
            return value.strip().lower() == __file__.strip().lower()
        return False
    except:
        return False
    return False

# Toggles the "Run at start" option
def toggle_run_at_start():
    try:
        if not does_run_at_start():
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run") as new_key:
                winreg.SetValueEx(new_key, "BatteryMonitor", 0, winreg.REG_SZ, __file__)
        else:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, "BatteryMonitor")
    except:
        None

    sysTrayIcon.update(menu_options = get_menu_options())

# tries to turn off the smart plug and shutdowns the computer
def shutdown():
    global running
    running = False
    if charger_is_plugged():
        plug(False, True)
    subprocess.Popen('shutdown -s -t 0', startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# reboots the computer
def reboot():
    subprocess.Popen('shutdown -r -t 0', startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# tries to turn off the smart plug, pauses the battery monitor and hibernates the computer
def hibernate():
    global paused
    paused = True
    if charger_is_plugged():
        plug(False, True)
    subprocess.Popen('shutdown -h', startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sl(3.5)
    paused = False

# Checking if there is a file path as an argument, if so have it open when this script is closed
caller = None
if len(argv) > 1:
    if path.exists(argv[1]):
        caller = path.realpath(argv[1])

def get_menu_options():
    if ping_domain:
        return (
            (f"Ping to {ping_domain}", None, lambda systray, num: system(f'ping {ping_domain} & TIMEOUT /T 6')),
            ("Open script dir", None, lambda systray, num: startfile(scr_path)),
            ("Run at start", scr_path + r'\icons\check.ico' if does_run_at_start() else None, lambda systray, num: toggle_run_at_start()),
            ("Shutdown", scr_path + r'\icons\shutdown.ico', lambda systray, num: shutdown()),
            ("Hibernate", scr_path + r'\icons\clock.ico', lambda systray, num: hibernate())
        )
    else:
        return (
            ("Open script dir", None, lambda systray, num: startfile(scr_path)),
            ("Run at start", scr_path + r'\icons\check.ico' if does_run_at_start() else None, lambda systray, num: toggle_run_at_start()),
            ("Shutdown", scr_path + r'\icons\shutdown.ico', lambda systray, num: shutdown()),
            ("Hibernate", scr_path + r'\icons\clock.ico', lambda systray, num: hibernate())
        )

sysTrayIcon = SysTrayIcon(scr_path + r'\icons\plug.ico', 'Battery Monitor', menu_options = get_menu_options(), on_quit = on_closing, default_menu_index = 0)
sysTrayIcon.start()

# Start battery monitor
start()
