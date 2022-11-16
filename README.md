# `Battery Monitor`

_**Version** 3.0.1_git

A simple Python script for **Windows** to monitor laptop battery percentage and prevent it from being too low or too high, helping to extend battery life. It works as a tray icon.

### Requirements
- **[infi.systray](https://github.com/Infinidat/infi.systray)**
```console
pip install infi.systray
```

### Usage

> To configure the script edit the _config.ini_ file

- You can set a domain to ping. Useful for gaming.
- You can configure two URLs so that the script makes a GET request when the percentage is less than the minimum or greater than the maximum set.
Designed to set up an IFTTT webhook to turn on/off a smart plug.
If no ON/OFF URLs are set, the script will make a double beep when the battery needs to be connected and a long beep when it needs to be disconnected.
- You can open it by setting the path to a file as an argument, closing the script will open the file. Intended to open the script from an application that needs to be closed and will reopen when the user closes the script.
```
batterymonitor.pyw "C:\OpenWhenClosing.exe"
```

### Attributions

[Plug icons created by Pixel perfect - Flaticon](https://www.flaticon.com/free-icons/plug)