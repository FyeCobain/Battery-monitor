from os import path, system
from re import sub, match
from sys import argv
from time import sleep
from urllib.request import urlopen, Request
from psutil import sensors_battery
from ruamel.yaml import YAML
system('cls')

#Set and write new current charging status
def setCharging(newChargingStatus):
    global charging
    global config
    charging = newChargingStatus
    config['charging'] = charging
    with open(configFile, 'w') as file:
        yaml.dump(config, file)

#Perform a simple GET request and return response data
def GET(url):
    try:
        with urlopen(Request(url)) as response:
            return (response.status, response.read().decode())
    except:
        return None

#Checks battery's current percent each 0.5 sec
running = True
def start():
    global running
    global charging
    while(running):
        #Getting battery info
        battery = sensors_battery()

        if(battery.percent < minPercent): #If min percent reached...
            setCharging(True)
        elif(battery.percent > maxPercent): #If max percent reached...
            setCharging(False)

        if(charging and not battery.power_plugged): #If battery must be connected...
            connect()
        elif(not charging and battery.power_plugged): #If battery must be disconnected...                plugOff()
            disconnect()
        else:
            print('ok')
        
        sleep(0.5)

#When the battery must be connected...
def connect():
    print(GET(onURL))
    sleep(5)

#When the battery must be disconnected...
def disconnect():
    print(GET(offURL))
    sleep(5)

#Getting current config as variables from the "config.yaml" file
configFile = sub('\\\\[^\\\\]*$', '', path.realpath(__file__)) + '\config.yaml'
yaml = YAML()
with open(configFile) as file:
    config = yaml.load(file)
    locals().update(config)

#Checking if there is a file as an argument, if so have it open when this script is closed
caller = None
callerPath = None
if len(argv) > 1:
    if path.exists(argv[1]):
        caller = path.realpath(argv[1])
        callerPath = sub('\\\\[^\\\\]*$', '', caller)
    print(caller)
    print(callerPath)

#If there's a "charging" status as argument, set it as current charging status
if len(argv) > 2:
    charging = True if match(r'(?i)^(?:1|true)$', argv[2]) else False
    setCharging(charging)
    print(argv[2])

#Start battery monitor
start()