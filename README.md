# `Battery Monitor`

_**Version** 5.0.0_

A Python script for **Windows** that monitors and controls the laptop's battery percentage, optionally with a smart plug, preventing it from getting too low or too high, thus helping to extend battery life. It functions as an icon in the system tray.

### Requirements
- **[simplesystray](https://github.com/actorpus/systrayv2)**
```console
pip install simplesystray
```

### Source Code
**[GitHub](https://github.com/FyeCobain/Battery-monitor)**

### Usage

> To configure the script edit the _config.ini_ file

- You can set a **domain** to ping. Useful for gaming.
- You can set two **URLs** so that the script makes a GET request when the percentage is less than the minimum or greater than the maximum allowed. Intended to set up an **IFTTT** webhook to turn **ON/OFF** a smart plug.

- You can set a Kasa token and device ID for the same result. Please refer to [this gist](https://gist.github.com/FyeCobain/1e367b0a9d5693c579a4fd6b20fac682).

If no ON/OFF **URLs** and no Kasa device are set, the script will play a sound when the battery needs to be connected or disconnected.

- You can open the script and pass it the path to a file. Closing the script will open that file. Intended to open the script from an application that needs to be closed and will be reopened when the user exits the script.
```
batterymonitor.pyw "C:\OpenWhenClosing.exe"
```

### Attributions

#### Icons

[Plug icons created by Pixel perfect - Flaticon](https://www.flaticon.com/free-icons/plug)

#### Sounds

<a href="https://freesound.org/people/mokasza/sounds/810739/">One-shot</a> by <a href="https://freesound.org/people/mokasza/">mokasza</a> | License: <a href="https://creativecommons.org/licenses/by/4.0/">Attribution 4.0</a>

<a href="https://freesound.org/people/Timbre/sounds/348976/">soft attack alert.wav</a> by <a href="https://freesound.org/people/Timbre/">Timbre</a> | License: <a href="https://creativecommons.org/licenses/by-nc/4.0/">Attribution NonCommercial 4.0</a>
