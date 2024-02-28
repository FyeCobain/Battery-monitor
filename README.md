# `Battery Monitor`

_**Version** 3.3.1_

A Python script for **Windows** to monitor and control laptop charge percentage and prevent it from being too low or too high, helping to extend battery lifetime. It works as a tray icon.

### Requirements
- **[infi.systray](https://github.com/Infinidat/infi.systray)**
```console
pip install infi.systray
```

#### Optional tool
- **[Smart Plug Switch](https://github.com/FyeCobain/Smart-Plug-Switch)**
(it requires [tinytuya](https://github.com/jasonacox/tinytuya))

### Usage

> To configure the script edit the _config.ini_ file

- You can set a **domain** to ping. Useful for gaming.
- You can set two **URLs** so that the script makes a GET request when the percentage is less than the minimum or greater than the maximum allowed. Intended to set up an **IFTTT** webhook, a **Tuya** endpoint or similar to turn **ON/OFF** a smart plug.
- You can also put the [Smart Plug Switch](https://github.com/FyeCobain/Smart-Plug-Switch) script in the same directory and add the required device information for the same or even a better result.

If no ON/OFF **URLs** and no **Smart Plug Switch** parameters are set, the script will make a **double beep** when the battery needs to be connected and a **long beep** when it needs to be disconnected.
- You can open it with the path to a file as an argument, closing the script will open that file. Intended to open the script from an application that needs to be closed and will be reopened when the user exits the script.
```
batterymonitor.pyw "C:\OpenWhenClosing.exe"
```

### Attributions

[Plug icons created by Pixel perfect - Flaticon](https://www.flaticon.com/free-icons/plug)