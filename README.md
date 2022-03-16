# Battery Monitor

_**Version** 1.0.0_

A simple python script for **Windows** to monitor laptop battery percentage and prevent it from being too low or too high, helping to extend battery life.

### Requirements
- **psutil**
```
pip install psutil
```
- **ruamel.yaml**
```
pip install ruamel.yaml
```
- **infi.systray**
```
pip install infi.systray
```

### Usage

- You can configure two URLs so that the script makes a GET request when the percentage is less than the minimum or greater than the maximum set.
Designed to set up an IFTTT webhook or Tuya link to turn on/off a smart plug.
If no URLs are set, the script will play an alert sound.
- You can open it and set as argument the path to a file, when closing the script, the file will be opened. Thought to open the script from an application that will be closed to avoid conflicts and must be reopened when the script is no longer needed.
```console
batterymonitor.py "C:\launchers\OpenWhenClosing.exe"
```

### Attributions

[Plug icons created by Pixel perfect - Flaticon](https://www.flaticon.com/free-icons/plug)