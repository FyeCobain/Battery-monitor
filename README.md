# Battery Monitor

A simple python script for Windows to monitor laptop battery percentage and prevent it from being too low or too high, helping to extend battery life.

You can configure two URLs so that the script makes a GET request when the percentage is less than the minimum or greater than the maximum set. Designed to set up an IFTTT webhook or Tuya link to turn on/off a smart plug.

If no URLs are set, the script will display an alert to the user.

## Requirements
> **psutil**
```
pip3 install psutil

```
> **ruamel.yaml**
```

pip3 install ruamel.yaml

```