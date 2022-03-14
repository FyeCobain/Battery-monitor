# Battery Monitor

_**Version** 0.1.0 (beta)_

A simple python script for Windows to monitor laptop battery percentage and prevent it from being too low or too high, helping to extend battery life.

### Requirements
> **psutil**
```
pip install psutil
```
> **ruamel.yaml**
```
pip install ruamel.yaml
```

### Usage

- You can configure two URLs so that the script makes a GET request when the percentage is less than the minimum or greater than the maximum set.
Designed to set up an IFTTT webhook or Tuya link to turn on/off a smart plug.
If no URLs are set, the script will display an alert to the user.
- You can open it and set as argument the path to a file, when closing the script, the file will be opened. Thought to open the script from an application that will be closed to avoid conflicts and will be opened again automatically.
```console
batterymonitor.py "C:\scripts\OpenWhenClosing.exe"
```