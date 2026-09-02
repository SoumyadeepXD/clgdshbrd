# Raspberry Pi Local Standalone Dashboard

A native, lightweight Python dashboard built specifically for **Raspberry Pi** that runs **100% locally without any external web browser** (no Chromium, no Electron).

It cycles between 3 screens (10s each):
1. **Time & Date**
2. **Weather of Kolkata (New Town)**
3. **Room Metrics (Noise dB, Room Humidity %, Air Quality AQI/PPM)**

---

## 🔌 Hardware Wiring Schematic & Pinout Guide

### Complete Pin-to-Pin Connection Diagram

```
       RASPBERRY PI 40-PIN GPIO HEADER
      ┌──────────────────────────────────┐
      │  (1) 3.3V  [PWR]  │ (2) 5V  [PWR]┼───────────┐ (5V Power Rail)
      │  (3) GPIO 2 [SDA] │ (4) 5V  [PWR]│           │
      │  (5) GPIO 3 [SCL] │ (6) GND [GND]┼────┐      │
      └───────┬──────┬──────────┬────────┘    │      │
              │      │          │             │      │
       ┌──────┘      │          └──────┐      │ (GND Rail)
       │ (SDA Line)  │ (SCL Line)      │      │      │
       ▼             ▼                 ▼      ▼      ▼
   ┌────────────────────────────────────────────────────────┐
   │                  ADS1115 / ADS1015 I2C ADC             │
   ├─────────┬─────────┬─────────┬──────────┬───────────────┤
   │   VDD   │   GND   │   SCL   │   SDA    │  ADDR         │
   └────┬────┴────┬────┴────┬────┴────┬─────┴───┬───────────┘
        │         │         │         │         │
    (3.3V Pin1) (GND Pin6) (SCL Pin5)(SDA Pin3)(GND Pin6)
                  │
                  │              ┌──────────────────────────┐
                  ├─────────────►│ MQ GAS SENSOR            │
                  │              ├──────────────────────────┤
                  │              │ VCC  ◄─── 5V (Pi Pin 2)  │
                  │              │ GND  ◄─── GND (Pi Pin 6) │
   ┌──────────────┼─────────────►│ AOUT ───► ADS1115 A0     │
   │              │              └──────────────────────────┘
   │              │              ┌──────────────────────────┐
   │              │              │ SOUND SENSOR             │
   │              │              ├──────────────────────────┤
   │              │              │ VCC  ◄─── 3.3V (Pi Pin 1)│
   │              │              │ GND  ◄─── GND (Pi Pin 6) │
   │              └─────────────►│ AOUT ───► ADS1115 A1     │
   │                             └──────────────────────────┘
   ▼
 ADS1115 Analog Input Channels:
   • Channel A0 ◄─── MQ Gas Sensor AOUT
   • Channel A1 ◄─── Sound Sensor AOUT
```

---

## 📌 Pinout Table

### 1. ADS1115 ADC $\rightarrow$ Raspberry Pi
| ADS1115 Pin | Raspberry Pi GPIO Pin | Physical Pin # | Description |
| :--- | :--- | :--- | :--- |
| **VDD** | 3.3V Power | **Pin 1** | Power Supply |
| **GND** | Ground | **Pin 6** | Ground Line |
| **SCL** | **GPIO 3 (SCL)** | **Pin 5** | **I2C Clock Line** |
| **SDA** | **GPIO 2 (SDA)** | **Pin 3** | **I2C Data Line** |
| **ADDR** | Ground | **Pin 6** | Sets I2C Address `0x48` |

### 2. MQ Gas Sensor
| MQ Sensor Pin | Connection Target | Description |
| :--- | :--- | :--- |
| **VCC** | Raspberry Pi **Pin 2 (5V)** | 5V Power for internal heater coil |
| **GND** | Raspberry Pi **Pin 6 (GND)** | Shared Ground |
| **AOUT** | ADS1115 **A0 Pin** | Analog Gas Output Signal |

### 3. Sound Decibel Sensor
| Sound Sensor Pin | Connection Target | Description |
| :--- | :--- | :--- |
| **VCC** | Raspberry Pi **Pin 1 (3.3V)** | 3.3V Power Supply |
| **GND** | Raspberry Pi **Pin 6 (GND)** | Shared Ground |
| **AOUT** | ADS1115 **A1 Pin** | Analog Sound Output Signal |

---

## ⚙️ Enabling I2C on Raspberry Pi

1. Open terminal on Raspberry Pi and run:
   ```bash
   sudo raspi-config
   ```
2. Go to **Interface Options** $\rightarrow$ **I2C** $\rightarrow$ **Enable**.
3. Reboot: `sudo reboot`
4. Test I2C detection:
   ```bash
   sudo i2cdetect -y 1
   ```
   *(You should see `48` at address `0x48`)*

---

## 🚀 Execution

```bash
cd ~/Developer/clgdshbrd
PI_DASHBOARD_FULLSCREEN=True .venv/bin/python main.py
```
