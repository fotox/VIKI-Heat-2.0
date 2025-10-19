# V.I.K.I-HEAT – Home Energy Management System
© by Fotox

![](documentation/landing_page.jpg)

A modular open-source **hardware & software platform** designed for intelligent energy and heating management at home.
This repository contains the documentation and setup instructions for the **hardware system** and its integration with the **V.I.K.I – Heat** software suite (frontend & backend).

> Status: **Open Source** project with basic functionalities under development and ready for further development.
---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Hardware Components](#hardware-components)
- [Bill of Materials (BOM)](#bill-of-materials-bom)
- [Installation & Wiring](#installation--wiring)
- [Software Installation (Raspberry Pi)](#software-installation-raspberry-pi)
- [Case & 3D Model](#case--3d-model)
- [First Start-Up Procedure](#first-start-up-procedure)
- [Testing the Temperature Sensors](#testing-the-temperature-sensors)
- [Safety Notes](#safety-notes)
- [Documentation References](#documentation-references)
- [License](#license)

---

## Overview

**V.I.K.I-HEAT – Home Energy Management System (HEMS)** provides a centralized platform to monitor, control, and
optimize heating and energy systems.
This part of the project focuses on the **hardware integration** — including temperature measurement, relay control,
and power distribution — built around a **Raspberry Pi 4**.

The system interfaces with the **V.I.K.I-HEAT** backend (Flask/Python) and frontend (React/TypeScript) to visualize
sensor data and control outputs in real time. For more information, read the
[README.md-Backend](function/backend/README.md) and the [README.md-Frontend](function/frontend/README.md).

---

## System Architecture

The hardware consists of several core modules:

- **Raspberry Pi 4** as the central controller
- **R4DCB08** module for Modbus-RTU communication with temperature sensors
- **3-way relay board** for controlling heating or auxiliary circuits
- **ABB F204 A** RCD (FI) and **ABB B16** circuit breakers for safety
- **Mean Well power supplies** for 5 V / 3 A (15 W) and 36 V / 1.5 A (36 W)
- **Heschen CT1-25** for switching heat pipes
- **DS18B20 temperature sensors** connected via the R4DCB08

All components are mounted inside a **three-row distribution cabinet**, powered by a **400 V / 64 A** main line.

Communication between the Raspberry Pi and the R4DCB08 occurs via a **USB–RS485 adapter** (Modbus RTU protocol).

---

## Hardware Components

| Component | Model / Type | Description                                               |
|------------|---------------|-----------------------------------------------------------|
| Control Unit | Raspberry Pi 4 (4 GB) | Central controller for system logic and API communication |
| Temperature Module | R4DCB08 | 8-channel Modbus-RTU temperature input board              |
| Sensors | DS18B20 | Digital temperature probes connected to R4DCB08           |
| Relay Board | 3-Channel Relay 5 V | Controls Current Switch                                   |
| Circuit Protection | ABB F204 A + 3× B16 + 1× B16 | RCD and circuit breakers for AC protection                |
| Power Supply 1 | Mean Well 15 W 5 V 3 A | Powers Raspberry Pi                                       |
| Power Supply 2 | Mean Well 36 W 36 V 1.5 A | Powers R4DCB08                                            |
| Current Switch | Heschen CT1-25 | Switch the energy flow to heat pipes                      |
| Communication | USB–RS485 Adapter | Connects R4DCB08 to Raspberry Pi serial port              |
| Cabinet | 3-Row Electrical Cabinet | Minimum 3 rows for DIN-rail components                    |
| Mounting | DIN-rail | Case and components mounted on standard DIN-rail          |

---

## Bill of Materials (BOM)

Below is a suggested list for constructing the complete **V.I.K.I – Heat hardware system**.

| Item                                          | Description                                          | Approx. Quantity | Cable Type              |
|-----------------------------------------------|------------------------------------------------------|------------------|-------------------------|
| Raspberry Pi 4 (4 GB)                         | Main control board                                   | 1                | –                       |
| R4DCB08 module                                | Modbus temperature reader                            | 1                | RS-485 cable, 2×0.5 mm² |
| USB–RS485 Adapter                             | Serial communication                                 | 1                | USB A                   |
| DS18B20 sensors                               | Temperature sensors                                  | 6 pcs            | Twisted-pair 2×0.5 mm²  |
| Relay Board (3-way)                           | Control output                                       | 1                | GPIO → HAT              |
| Mean Well 5 V 3 A PSU                         | Low-voltage PSU                                      | 1                | 230 V → 5 V             |
| Mean Well 36 V 1.5 A PSU                      | Secondary PSU                                        | 1                | 230 V → 36 V            |
| ABB F204 A                                    | 4-pole RCD                                           | 1                | 400 V → main feed       |
| ABB B16 Breakers                              | 16 A protection                                      | 4                | 230 V branch circuits   |
| Heschen CT1-25                                | Current relay                                        | 3                | 1,5 mm² Copper          |
| Cabinet ≥ 3 rows                              | Electrical housing                                   | 1                | –                       |
| Mounting rails, screws, connectors            | For assembly                                         | as required      | –                       |
| RJ45 cable and adapter with platform mounting | Transition between switch cabinet inside and outside | as required      | RJ45                    |
| Wires (400 V side)                            | Load                                                 | 1                | 6 mm² Copper            |
| Wires (230 V side)                            | Supply / Relay / Load                                | –                | 1,5 mm² Copper          |
| Low-voltage wiring                            | RS485 / GPIO / Sensors                               | –                | 0.25–0.5 mm² Copper     |

> ⚙️ *Cable lengths depend on installation; use proper color coding and ensure sufficient isolation.*

---

## Installation & Wiring

Detailed schematics and wiring diagrams are provided in:

- [documentation/eplan.pdf](documentation/eplan.pdf) – Full electrical schematic
- [documentation/wiring.pdf](documentation/wiring.pdf) – Visual wiring diagram with component layout

### Summary

1. Mount all components inside a **three-row DIN-rail cabinet**.
2. Wire the **Mean Well** power supplies to distribute 5 V / 36 V lines.
3. Connect the **Raspberry Pi 4** to:
   - R4DCB08 via **USB–RS485 adapter**
   - Relay board via **GPIO pins**
   - Power via the 5 V supply
4. Attach **temperature sensors** to the R4DCB08 according to the Modbus address mapping.
5. Connect the **400 V feed** through the ABB F204 A FI and circuit breakers.
6. Verify wiring continuity and polarity before energizing the system.

> 🧠 **Note:** All RS485 and signal lines should be shielded to avoid interference.
> Keep high-voltage and low-voltage cables separated in the cabinet.

---

## Software Installation (Raspberry Pi)

After the wiring is complete, the Raspberry Pi must be prepared with the required libraries and runtime environment.

### 1. Install BCM2835 Library

The BCM2835 library is required for low-level GPIO access and relay control.

```bash
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
tar zxvf bcm2835-1.71.tar.gz
cd bcm2835-1.71/
sudo ./configure && sudo make && sudo make check && sudo make install
```

### 2. Install Docker

Docker is used to run the backend and frontend containers for the V.I.K.I-HEAT system.

```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

After re-login, you can verify installation with:

```bash
docker --version
```
### 3. Install Required Python Libraries

The R4DCB08 temperature module requires pymodbus and pyserial.

```bash
sudo apt update
sudo apt install python3-pip python3-pymodbus python3-serial
```

Once completed, the system is ready to run the V.I.K.I-HEAT Docker containers.

## Case & 3D Model

The V.I.K.I Heat hardware case consists of a base and lid printed in PETG (white + blue).

- Mounting type: DIN-rail (inside electrical cabinet)

3D and construction files:

- [CASE](documentation/case.3mf) – 3D model (print-ready)
- [Technical Overview Base](documentation/technical_map_case_base.pdf) – Base plate construction plan
- [Technical Overview Top](documentation/technical_map_case_top.pdf) – Top cover construction plan

## First Start-Up Procedure

1. Connect the RJ-45 communication cable on the top side.
2. Switch on the FI and circuit breakers.
3. Boot the Raspberry Pi with the micro-SD containing the [V.I.K.I–HEAT](documentation/viki_heat.img) image.
4. Ensure BCM2835 and Docker are correctly running (see section above).
5. Access the web interface via your network using the Pi’s IP address on port 80.
6. Configure your household and heating parameters in the Settings section.
7. Verify temperature readings in the dashboard.

The system currently operates via Ethernet only.
WLAN functionality is planned for future revisions.

## Testing the Temperature Sensors

There are two main ways to test the temperature readings:

### Option 1 – Using the Frontend Dashboard

Sensor values appear on the dashboard under Heating → Temperature Sensors once the backend service is active.

### Option 2 – Using the Shell Script

Run the provided Python script on the Raspberry Pi to verify Modbus readings manually:

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

You should see temperature values for all connected DS18B20 sensors printed to the terminal.

If no values appear, verify RS485 connections and Modbus addressing on the R4DCB08.

## Safety Notes

⚠️ Electrical Safety Warning

This system operates at 400 V AC and must be installed only by a qualified electrician.
All wiring and installation of FI and power supplies must comply with local electrical regulations.

- Always disconnect power before wiring or service.
- Use appropriate wire gauges (1.5 mm² min for 230 V).
- Ensure all protective earth (PE) connections are continuous.
- Keep signal and power cables separated.

Improper installation can result in electric shock, fire, or equipment damage.

## Documentation References

- Electrical plan: [documentation/eplan.pdf](documentation/Eplan.pdf)
- Wiring diagram: [documentation/wiring.pdf](documentation/wiring.pdf)
- 3D model: [documentation/case.3mf](documentation/case.3mf)
- Case base: [documentation/technical_map_case_base.pdf](documentation/technical_map_case_base.pdf)
- Case head: [documentation/technical_map_case_top.pdf](documentation/technical_map_case_top.pdf.pdf)
- Software setup: see
  - [function/frontend/README.md](function/frontend/README.md)
  - [function/backend/README.md](function/backend/README.md)

## License

This hardware documentation and associated software are licensed under the MIT License.
See the [LICENSE](LICENSE) file for full terms.
