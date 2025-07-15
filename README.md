# Install R4DCB08

## Schritt 1: Serielle Kommunikation vorbereiten
Verbinde das R4DCB08-Modul über den USB-RS485-Adapter mit deinem Raspberry Pi.

Aktiviere die serielle Schnittstelle auf dem Raspberry Pi:

Öffne das Konfigurationstool:
```bash
sudo raspi-config

Interfacing Options -> Serial und deaktiviere die serielle Konsole, aktiviere aber die serielle Schnittstelle.

```
Installiere das Paket pymodbus, das für die Modbus-Kommunikation benötigt wird:
```bash
sudo apt update
sudo apt install python3-pip python3-pymodbus python3-serial
```

## Schritt 2: Python-Code zum Auslesen der Temperaturdaten
Verwende das folgende Python-Skript, um die Temperatursensoren auszulesen. Das Skript verwendet die pymodbus-Bibliothek, um Modbus-RTU-Kommunikation über die serielle Schnittstelle durchzuführen.

Erstelle eine Python-Datei:
```bash
nano r4dcb08_read.py
```

Füge den folgenden Code in die Datei ein:

```python
import time

from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.pdu import ModbusPDU

temp_sensors: dict = {
    "Sensor 1": {
      "binding": "buffer_tank_higher_sensor",
      "name": "Warmwasserspeicher Oben",
      "value": 0
    },
    "Sensor 2": {
      "binding": "buffer_tank_middle_sensor",
      "name": "Warmwasserspeicher Mitte",
      "value": 0
    },
    "Sensor 3": {
      "binding": "buffer_tank_upper_sensor",
      "name": "Warmwasserspeicher Unten",
      "value": 0
    },
    "Sensor 4": {
      "binding": "",
      "name": "Pufferspeicher Oben",
      "value": 0
    },
    "Sensor 5": {
      "binding": "",
      "name": "Pufferspeicher Mitte",
      "value": 0
    },
    "Sensor 6": {
      "binding": "",
      "name": "Pufferspeicher Unten",
      "value": 0
    }
}
client = ModbusClient(port='/dev/ttyS0', baudrate=9600, timeout=1, parity='N', stopbits=1, bytesize=8)

if not client.connect():
    print("No connection to R4DCB08 module.")
    print(temp_sensors)

try:
    response: ModbusPDU = client.read_holding_registers(0x0000, 8, slave=1)
    if not response.isError():
        temperatures: list[int] = response.registers
        for i, temp in enumerate(temperatures[:6]):
            if temp < 30000:
                temp_sensors['Sensor ' + str(i + 1)]['value'] = temp / 10.0
            else:
                temp_sensors['Sensor ' + str(i + 1)]['value'] = 0
        client.close()
        print(f"Read temperature sensors successfully. Values: {temp_sensors}")
        print(temp_sensors)

    else:
        print("Error by reading the R4DCB08 register.")
    time.sleep(2)

except Exception as e:
    print(f"Error by reading sensor: {e}")
```

## Schritt 3: Skript ausführen
Führe das Python-Skript aus:

```bash
python3 r4dcb08_read.py
```

Du solltest nun die Temperaturwerte der angeschlossenen DS18B20-Sensoren im Terminal sehen.


# Install RPi Relay Board 3-way

## Schritt 1: Install BCM2835

Open the Raspberry Pi terminal and run the following command

```bash
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
tar zxvf bcm2835-1.71.tar.gz
cd bcm2835-1.71/
sudo ./configure && sudo make && sudo make check && sudo make install
```
For more information, please refer to the official website: http://www.airspayce.com/mikem/bcm2835/


# Button and LED Basis

```python
from gpiozero import LED, Button
from time import sleep

button_wifi = Button(12)
button_state = Button(16)
led_wifi = LED(19)
led_state = LED(13)

while True:
    print(f"LED WIFI: {led_wifi.is_active}")
    print(f"LED STATE: {led_state.is_active}")

    if button_wifi.is_pressed:
        if led_wifi.is_active is True:
            led_wifi.off()
        else:
            led_wifi.on()
        print("Button Wifi is pressed")

    if button_state.is_pressed:
        if led_state.is_active is True:
            led_state.off()
        else:
            led_state.on()
        print("Button State is pressed")
    sleep(1)
```

# Install V.I.K.I - Heat App

Open the Raspberry Pi terminal and run the following command

```bash
sudo apt install python3-flask
sudo mkdir /viki
sudo mkdir /viki/heat
```

Copy code to /viki/heat

```bash
python3 /viki/heat/app.py &
```


# Install V.I.K.I - WiFi-Connect

Open the Raspberry Pi terminal and run the following command

```bash
sudo mkdir /viki/wifi-manager
```

Copy code to /viki/wifi-manager

To test the code run:
```bash
python3 /viki/wifi-manager/app.py &
```

Add viki-wifi-manager to rc.local
```bash
sudo nano /etc/rc.local
```

```bash
#!/bin/sh -e
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

python3 /viki/wifi-manager/main.py &
python3 /viki/heat/app.py &

exit 0
```

# Docker
## Install on raspberry pi

```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
logout
```

## Docker Image
### Build / Save / Load / Run

!Important: Before saving, change from powershell to cmd console. When the save command runs in the powershell console,
the error "archive/tar: invalid tar header" code comas when your want to load the image on the raspberry pi.

```bash
docker build --platform linux/arm64 -t viki-heat_arm:<VERSIONSNUMMER> -t viki-heat:latest .
docker save viki-heat:latest > viki-heat.tar
docker load < viki-heat_<VERSIONSNUMMER>.tar.gz
docker-compose up -d
```
