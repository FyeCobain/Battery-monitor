# `Battery Monitor`

_**Version** 1.2.1_

A simple python script for **Windows** to monitor laptop battery percentage and prevent it from being too low or too high, helping to extend battery life. It works as tray icon.

### Requirements
- **psutil**
```console
pip install psutil
```
- **ruamel.yaml**
```console
pip install ruamel.yaml
```
- **infi.systray**
```console
pip install infi.systray
```

### Usage

> To configure the script edit the _config.yaml_ file

- You can specify a domain to ping. Useful for gaming.
- You can configure two URLs so that the script makes a GET request when the percentage is less than the minimum or greater than the maximum set.
Designed to set up an IFTTT webhook or Tuya link to turn on/off a smart plug.
If no ON/OFF URLs are set, the script will play an alert sound instead.
- You can open it and set as argument the path to a file, when closing the script, the file will be opened. Thought to open the script from an application that must be closed and will be reopened when the script is no longer needed.
```
batterymonitor.pyw "C:\OpenWhenClosing.exe"
```

### Attributions

[Plug icons created by Pixel perfect - Flaticon](https://www.flaticon.com/free-icons/plug)
